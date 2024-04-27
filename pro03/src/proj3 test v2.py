from ants import *
from ants_plans import *
import unittest
import sys
import io
import importlib
class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.old_thrower_action = ThrowerAnt.action
        self.old_throw_at = ThrowerAnt.throw_at
        return super().setUp()
    
    def test1(self):
        # Testing HarvesterAnt action
        # Create a test layout where the colony is a single row with 9 tiles
        beehive = Hive(make_test_assault_plan())
        gamestate = GameState(None, beehive, ant_types(), dry_layout, (1, 9))
        #
        gamestate.food = 4
        harvester = HarvesterAnt()
        # Note that initializing an Ant here doesn't cost food, only
        # deploying an Ant in the game simulation does
        self.assertEqual(Ant.food_cost, 0)
        self.assertEqual(HarvesterAnt.food_cost, 2)
        self.assertEqual(ThrowerAnt.food_cost, 3)
        self.assertEqual(gamestate.food, 4)
        harvester.action(gamestate)
        self.assertEqual(gamestate.food, 5)
        harvester.action(gamestate)
        self.assertEqual(gamestate.food, 6)
        self.assertEqual(HarvesterAnt.implemented, True)
          
    def test2_1(self):
        # Simple test for Place
        place0 = Place('place_0')
        self.assertEqual(None, place0.exit)
        self.assertEqual(None, place0.entrance)
        place1 = Place('place_1', place0)
        self.assertEqual(place1.exit is place0, True)
        self.assertEqual(place0.entrance is place1, True)
    
    def test2_2(self):
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 3)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing if entrances are properly initialized
        tunnel_len = 9
        self.assertEqual(1, len(gamestate.bee_entrances))
        tile_1 = gamestate.bee_entrances[0]
        tile_2 = tile_1.exit
        tile_3 = tile_2.exit
        
        self.assertEqual(True, tile_1.entrance is gamestate.beehive)
        self.assertEqual(True, tile_1.exit is tile_2)
        self.assertEqual(True, tile_2.entrance is tile_1)
        self.assertEqual(True, tile_2.exit is tile_3)
        self.assertEqual(True, tile_3.entrance is tile_2)
        self.assertEqual(True, tile_3.exit is gamestate.base)
    
    def test3_1(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Testing nearest_bee
        near_bee = Bee(2) # A Bee with 2 health
        far_bee = Bee(3)  # A Bee with 3 health
        hive_bee = Bee(4) # A Bee with 4 health
        hive_place = gamestate.beehive
        
        self.assertEqual(True, hive_place.is_hive, "Check if this place is the Hive") # Check if this place is the Hive

        hive_place.add_insect(hive_bee)
        
        self.assertEqual(False, thrower.nearest_bee() is hive_bee) # Bees in the Hive can never be attacked
        near_place = gamestate.places['tunnel_0_3']
        far_place = gamestate.places['tunnel_0_6']
        
        self.assertEqual(False, near_place.is_hive, "Check if this place is the Hive") # Check if this place is the Hive
        near_place.add_insect(near_bee)
        far_place.add_insect(far_bee)
        nearest_bee = thrower.nearest_bee()
        
        self.assertEqual(False, nearest_bee is far_bee)
        self.assertEqual(True, nearest_bee is near_bee)
        self.assertEqual(2, nearest_bee.health)
        thrower.action(gamestate)    # Attack! ThrowerAnts do 1 damage
        self.assertEqual(1, near_bee.health)
        self.assertEqual(3, far_bee.health)
        self.assertEqual(True, thrower.place is ant_place, "Don't change self.place!") # Don't change self.place!
    
    def test3_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Testing Nearest bee not in the beehive
        beehive = gamestate.beehive
        bee = Bee(2)
        beehive.add_insect(bee)      # Adding a bee to the beehive
        self.assertEqual(False, thrower.nearest_bee() is bee)
        thrower.action(gamestate)    # Attempt to attack
        self.assertEqual(bee.health, 2, "Bee health should not change") # Bee health should not change

    def test3_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Test that ThrowerAnt attacks bees on its own square
        near_bee = Bee(2)
        ant_place.add_insect(near_bee)
        self.assertEqual(True, thrower.nearest_bee() is near_bee)
        thrower.action(gamestate)   # Attack!
        self.assertEqual(near_bee.health, 1, "should do 1 damage") # should do 1 damage

    def test3_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Test that ThrowerAnt attacks bees at end of tunnel
        near_bee = Bee(2)
        gamestate.places["tunnel_0_8"].add_insect(near_bee)
        
        self.assertEqual(True, thrower.nearest_bee() is near_bee)
        thrower.action(gamestate)   # Attack!
        self.assertEqual(1, near_bee.health) # should do 1 damage

    def test3_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Test that ThrowerAnt attacks bees 4 places away
        near_bee = Bee(2)
        gamestate.places["tunnel_0_4"].add_insect(near_bee)
        self.assertEqual(True, thrower.nearest_bee() is near_bee)
        thrower.action(gamestate)   # Attack!
        self.assertEqual(1, near_bee.health) # should do 1 damage

    def test3_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        thrower = ThrowerAnt()
        ant_place = gamestate.places["tunnel_0_0"]
        ant_place.add_insect(thrower)

        # Testing ThrowerAnt chooses a random target
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        gamestate.places["tunnel_0_3"].add_insect(bee1)
        gamestate.places["tunnel_0_3"].add_insect(bee2)
        # Throw 1000 times. The first bee should take ~1000*1/2 = ~500 damage,
        # and have ~501 remaining.
        for _ in range(1000):
            thrower.action(gamestate)
        # Test if damage to bee1 is within 6 standard deviations (~95 damage)
        # If bees are chosen uniformly, this is true 99.9999998% of the time.
        def dmg_within_tolerance():
            return abs(bee1.health-501) < 95
        
        self.assertEqual(True, dmg_within_tolerance())
    
    def test4_1(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        
        # Testing Long/ShortThrower parameters
        self.assertEqual(2, ShortThrower.food_cost)
        self.assertEqual(2, LongThrower.food_cost)
        short_t = ShortThrower()
        long_t = LongThrower()
        
        self.assertEqual(1, short_t.health)
        self.assertEqual(1, long_t.health)
        
        self.assertEqual(True, LongThrower.implemented)
        self.assertEqual(True, ShortThrower.implemented)

    def test4_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Test ShortThrower hit
        ant = ShortThrower()
        in_range = Bee(2)
        gamestate.places['tunnel_0_0'].add_insect(ant)
        gamestate.places["tunnel_0_3"].add_insect(in_range)
        ant.action(gamestate)
        self.assertEqual(in_range.health, 1)

    def test4_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing ShortThrower miss
        ant = ShortThrower()
        out_of_range = Bee(2)
        gamestate.places["tunnel_0_0"].add_insect(ant)
        gamestate.places["tunnel_0_4"].add_insect(out_of_range)
        ant.action(gamestate)
        
        self.assertEqual(2, out_of_range.health)

    def test4_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Test LongThrower Hit
        ant = LongThrower()
        in_range = Bee(2)
        gamestate.places['tunnel_0_0'].add_insect(ant)
        gamestate.places["tunnel_0_5"].add_insect(in_range)
        ant.action(gamestate)
        
        self.assertEqual(1, in_range.health)
        
    def test4_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing LongThrower miss
        ant = LongThrower()
        out_of_range = Bee(2)
        gamestate.places["tunnel_0_0"].add_insect(ant)
        gamestate.places["tunnel_0_4"].add_insect(out_of_range)
        ant.action(gamestate)
        
        self.assertEqual(2, out_of_range.health)

    def test4_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing LongThrower miss next to the hive
        ant = LongThrower()
        gamestate.places["tunnel_0_4"].add_insect(ant)
        ant.action(gamestate) # should not error

    def test4_7(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing LongThrower targets farther one
        ant = LongThrower()
        out_of_range = Bee(2)
        in_range = Bee(2)
        gamestate.places["tunnel_0_0"].add_insect(ant)
        gamestate.places["tunnel_0_4"].add_insect(out_of_range)
        gamestate.places["tunnel_0_5"].add_insect(in_range)
        ant.action(gamestate)
        
        self.assertEqual(2, out_of_range.health)
        self.assertEqual(1, in_range.health)

    def test4_8(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing LongThrower ignores bees outside range
        thrower = LongThrower()
        gamestate.places["tunnel_0_0"].add_insect(thrower)
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        gamestate.places["tunnel_0_4"].add_insect(bee1)
        gamestate.places["tunnel_0_5"].add_insect(bee2)
        thrower.action(gamestate)
        
        self.assertEqual(1001, bee1.health)
        self.assertEqual(1000, bee2.health)

    def test4_9(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing LongThrower attacks nearest bee in range
        thrower = LongThrower()
        gamestate.places["tunnel_0_0"].add_insect(thrower)
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        gamestate.places["tunnel_0_5"].add_insect(bee1)
        gamestate.places["tunnel_0_6"].add_insect(bee2)
        thrower.action(gamestate)
        
        self.assertEqual(1000, bee1.health)
        self.assertEqual(1001, bee2.health)

    def test4_10(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing case when min_range of LongThrower is outside of the tunnel
        bee = Bee(2)
        ant = LongThrower()
        gamestate.places["tunnel_0_6"].add_insect(ant)
        gamestate.places["tunnel_0_7"].add_insect(bee)
        ant.action(gamestate)
        
        self.assertEqual(2, bee.health)

    def test4_11(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing if max_range is looked up in the instance
        # and check that the code isnt dependent on the ants name
        ant = ShortThrower()
        ant.name = 'short2'
        ant.max_range = 10   # Buff the ant's range
        gamestate.places["tunnel_0_0"].add_insect(ant)
        bee = Bee(2)
        gamestate.places["tunnel_0_6"].add_insect(bee)
        ant.action(gamestate)
                
        self.assertEqual(1, bee.health)

    def test4_12(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing there is no new nearest_bee function in ShortThrower / LongThrower        
        self.assertEqual(True, ShortThrower.nearest_bee is ThrowerAnt.nearest_bee)
        self.assertEqual(True, LongThrower.nearest_bee is ThrowerAnt.nearest_bee)

    def test5_1(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()

        # Testing FireAnt parameters
        fire = FireAnt()
        self.assertEqual(5, FireAnt.food_cost)
        self.assertEqual(3, fire.health)

        # Abstraction tests
        original = Ant.__init__
        Ant.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
        fire = FireAnt()
        self.assertEqual('init\n', sys.stdout.getvalue())
        sys.stdout = io.StringIO()

        
        Ant.__init__ = original
        fire = FireAnt()
        original = Ant.reduce_health
        Ant.reduce_health = lambda self, amount: print("reduced") #If this errors, you are not calling the inherited method correctly
        place = gamestate.places['tunnel_0_4']
        place.add_insect(fire)
        fire.reduce_health(1)

        self.assertEqual('reduced\n', sys.stdout.getvalue())
        sys.stdout = io.StringIO()
        Ant.reduce_health = original

    def test5_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()

        # Testing fire does damage to all Bees in its Place
        place = gamestate.places['tunnel_0_4']
        fire = FireAnt(health=1)
        place.add_insect(fire)        # Add a FireAnt with 1 health
        place.add_insect(Bee(3))      # Add a Bee with 3 health
        place.add_insect(Bee(5))      # Add a Bee with 5 health

        self.assertEqual(2, len(place.bees)) # How many bees are there?
        place.bees[0].action(gamestate)  # The first Bee attacks FireAnt
        
        self.assertEqual(0, fire.health)
        
        self.assertEqual(True, fire.place is None)
        self.assertEqual(1, len(place.bees))    # How many bees are left?
        self.assertEqual(place.bees[0].health, 1)   # What is the health of the remaining Bee?

        place = gamestate.places['tunnel_0_4']
        ant = FireAnt(health=1)           # Create a FireAnt with 1 health
        place.add_insect(ant)      # Add a FireAnt to place
        self.assertEqual(True, ant.place is place)
        place.remove_insect(ant)   # Remove FireAnt from place
        self.assertEqual(False, ant.place is place) # Is the ant's place still that place?

    def test5_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # Testing fire damage when the fire ant does not die
        place = gamestate.places['tunnel_0_4']
        bee = Bee(5)
        ant = FireAnt(health=100)
        place.add_insect(bee)
        place.add_insect(ant)
        bee.action(gamestate) # attack the FireAnt
        
        self.assertEqual(99, ant.health)
        self.assertEqual(4, bee.health)

    def test5_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # Testing no hardcoded 3
        place = gamestate.places['tunnel_0_4']
        bee = Bee(100)
        ant = FireAnt(health=1)
        ant.damage = 49
        place.add_insect(bee)
        place.add_insect(ant)
        bee.action(gamestate) # attack the FireAnt
        
        self.assertEqual(0, ant.health)
        self.assertEqual(50, bee.health)

    def test5_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # Testing fire damage when the fire ant does die
        place = gamestate.places['tunnel_0_4']
        bee = Bee(5)
        ant = FireAnt(health=1)
        place.add_insect(bee)
        place.add_insect(ant)
        bee.action(gamestate) # attack the FireAnt
        
        self.assertEqual(0, ant.health)
        self.assertEqual(bee.health, 1)

    def test5_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # Testing fire does damage to all Bees in its Place
        place = gamestate.places['tunnel_0_4']
        place.add_insect(FireAnt(1))
        for i in range(100):          # Add 100 Bees with 3 health
            place.add_insect(Bee(3))
        place.bees[0].action(gamestate)  # The first Bee attacks FireAnt
        self.assertEqual(len(place.bees), 0)    # How many bees are left?

    def test5_7(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # Testing fire damage is instance attribute
        place = gamestate.places['tunnel_0_4']
        bee = Bee(900)
        buffAnt = FireAnt(1)
        buffAnt.damage = 500   # Feel the burn!
        place.add_insect(bee)
        place.add_insect(buffAnt)
        bee.action(gamestate) # attack the FireAnt
        self.assertEqual(399, bee.health)   # is damage an instance attribute?

    def test5_8(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # General FireAnt Test
        place = gamestate.places['tunnel_0_4']
        bee = Bee(10)
        ant = FireAnt(1)
        place.add_insect(bee)
        place.add_insect(ant)
        bee.action(gamestate)    # Attack the FireAnt
        self.assertEqual(bee.health, 6)
        self.assertEqual(ant.health, 0)
        self.assertEqual(place.ant is None, True)     # The FireAnt should not occupy the place anymore
        bee.action(gamestate)
        self.assertEqual(bee.health, 6)             # Bee should not get damaged again
        self.assertEqual(bee.place.name, 'tunnel_0_3')    # Bee should not have been blocked

    def test5_9(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # General FireAnt Test
        place = gamestate.places['tunnel_0_4']
        bee = Bee(10)
        ant = FireAnt()
        place.add_insect(bee)
        place.add_insect(ant)
        ant.reduce_health(0.1) # Poke the FireAnt
        self.assertEqual(9.9, bee.health) #  Bee should only get slightly damaged
        self.assertEqual(ant.health, 2.9)
        self.assertEqual(place.ant is ant, True)      # The FireAnt should still be at place

    def test5_10(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)        
        
        sys.stdout = io.StringIO()
        # test proper call to death callback
        original_death_callback = Insect.death_callback
        Insect.death_callback = lambda x: print("insect died")
        place = gamestate.places["tunnel_0_0"]
        bee = Bee(3)
        ant = FireAnt()
        place.add_insect(bee)
        place.add_insect(ant)
        bee.action(gamestate)
        bee.action(gamestate)
        bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
        self.assertEqual(sys.stdout.getvalue(), 'insect died\ninsect died\n')
        
        Insect.death_callback = original_death_callback
    
    def test5_11(self):
        self.assertEqual(FireAnt.implemented, True)
    
    def test6_1(self):
        # Testing WallAnt parameters
        wall = WallAnt()
        self.assertEqual(wall.name, 'Wall')
        self.assertEqual(wall.health, 4)
        # `health` should not be a class attribute
        self.assertEqual(not hasattr(WallAnt, 'health'), True) # hasattr checks if the WallAnt class has a class attribute called 'health'
        self.assertEqual(4, WallAnt.food_cost)

    def test6_2(self):
        # Abstraction tests
        original = Ant.__init__
        Ant.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
        sys.stdout = io.StringIO()
        wall = WallAnt()
        self.assertEqual('init\n', sys.stdout.getvalue())

        Ant.__init__ = original
        wall = WallAnt()

    def test6_3(self):
        # Testing WallAnt holds strong
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
        place = gamestate.places['tunnel_0_4']
        wall = WallAnt()
        bee = Bee(1000)
        place.add_insect(wall)
        place.add_insect(bee)
        for i in range(3):
            bee.action(gamestate)
            wall.action(gamestate)   # WallAnt does nothing

        self.assertEqual(wall.health, 1)
        self.assertEqual(bee.health, 1000)
        self.assertEqual(wall.place is place, True)
        self.assertEqual(bee.place is place, True)

    def test7_1(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt parameters
        hungry = HungryAnt()
        self.assertEqual(HungryAnt.food_cost, 4)
        self.assertEqual(hungry.health, 1)
        self.assertEqual(hungry.chew_duration, 3)
        self.assertEqual(hungry.chew_countdown, 0)

    def test7_2(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Abstraction tests
        original = Ant.__init__
        Ant.__init__ = lambda self, health: print("init")  # If this errors, you are not calling the parent constructor correctly.
        
        sys.stdout = io.StringIO()
        hungry = HungryAnt()
        self.assertEqual('init\n', sys.stdout.getvalue())
        sys.stdout = io.StringIO()

        Ant.__init__ = original
        hungry = HungryAnt()
        # Class vs Instance attributes
        self.assertEqual(hasattr(HungryAnt, 'chew_countdown'), False)  # chew_countdown should be an instance attribute
        self.assertEqual(hungry.chew_countdown, 0)  # HungryAnt is ready to eat a bee
        self.assertEqual(HungryAnt.chew_duration, 3)

    def test7_3(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt eats and chews
        hungry = HungryAnt()
        bee1 = Bee(1000)              # A Bee with 1000 health
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(hungry)
        place.add_insect(bee1)         # Add the Bee to the same place as HungryAnt
        hungry.action(gamestate)
        self.assertEqual(bee1.health, 0)
        bee2 = Bee(1)                 # A Bee with 1 health
        place.add_insect(bee2)
        for _ in range(3):
            hungry.action(gamestate)     # Digesting...not eating
        self.assertEqual(bee2.health, 1)
        hungry.action(gamestate)
        self.assertEqual(bee2.health, 0)

    def test7_4(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt eats and chews
        hungry = HungryAnt()
        super_bee, wimpy_bee = Bee(1000), Bee(1)
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(hungry)
        place.add_insect(super_bee)
        hungry.action(gamestate)         # super_bee is no match for HungryAnt!
        self.assertEqual(super_bee.health, 0)
        place.add_insect(wimpy_bee)
        for _ in range(3):
            hungry.action(gamestate)     # chewing...not eating
        self.assertEqual(wimpy_bee.health, 1)
        hungry.action(gamestate)         # back to eating!
        self.assertEqual(wimpy_bee.health, 0)

    def test7_5(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt only waits when chewing
        hungry = HungryAnt()
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(hungry)
        # Wait a few turns before adding Bee
        for _ in range(5):
            hungry.action(gamestate)  # shouldn't be chewing
        bee = Bee(3)
        place.add_insect(bee)
        hungry.action(gamestate)  # Eating time!
        self.assertEqual(bee.health, 0)
        bee = Bee(3)
        place.add_insect(bee)
        for _ in range(3):
            hungry.action(gamestate)     # Should be chewing
        self.assertEqual(bee.health, 3)
        hungry.action(gamestate)
        self.assertEqual(bee.health, 0)

    def test7_6(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt chew duration looked up on instance
        very_hungry = HungryAnt()  # Add very hungry caterpi- um, ant
        HungryAnt.chew_duration = 0
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(very_hungry)
        for _ in range(100):
            place.add_insect(Bee(3))
        for _ in range(100):
            very_hungry.action(gamestate)   # Eat all the bees!
        self.assertEqual(len(place.bees), 0)

    def test7_7(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt dies while eating
        hungry = HungryAnt()
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(hungry)
        place.add_insect(Bee(3))
        hungry.action(gamestate)
        self.assertEqual(len(place.bees), 0)

        bee = Bee(3)
        place.add_insect(bee)
        bee.action(gamestate) # Bee kills chewing ant
        self.assertEqual(place.ant is None, True)
        self.assertEqual(len(place.bees), 1)

    def test7_8(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt can't eat a bee at another space
        hungry = HungryAnt()
        gamestate.places["tunnel_0_0"].add_insect(hungry)
        gamestate.places["tunnel_0_1"].add_insect(Bee(3))
        hungry.action(gamestate)
        self.assertEqual(len(gamestate.places["tunnel_0_1"].bees), 1)

    def test7_9(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # test proper call to death callback
        original_death_callback = Insect.death_callback
        Insect.death_callback = lambda x: print("insect died")
        ant = HungryAnt()
        bee = Bee(1000)              # A Bee with 1000 health
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(bee)
        place.add_insect(ant)
        sys.stdout = io.StringIO()
        ant.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
        self.assertEqual('insect died\n', sys.stdout.getvalue())
        Insect.death_callback = original_death_callback

    def test7_10(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing HungryAnt removes bee when eating.
        hungry = HungryAnt()
        place = gamestate.places["tunnel_0_0"]
        place.add_insect(hungry)
        place.add_insect(Bee(3))
        place.add_insect(Bee(3))
        hungry.action(gamestate)
        self.assertEqual(len(place.bees), 1)
        bee = Bee(3)
        place.add_insect(bee)
        bee.action(gamestate) # Bee kills chewing ant
        self.assertEqual(place.ant is None, True)
        self.assertEqual(len(place.bees), 2)
    
    def test8_1(self):
        # Testing BodyguardAnt parameters
        bodyguard = BodyguardAnt()
        self.assertEqual(BodyguardAnt.food_cost, 4)
        self.assertEqual(bodyguard.health, 2)
        
    def test8_2(self):        
        # Abstraction tests
        original = ContainerAnt.__init__
        ContainerAnt.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
        sys.stdout = io.StringIO()
        bodyguard = BodyguardAnt()
        self.assertEqual('init\n', sys.stdout.getvalue())
        ContainerAnt.__init__ = original
        bodyguard = BodyguardAnt()
        self.assertEqual(hasattr(bodyguard, 'ant_contained'), True)        
    
    def test8_3(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        bodyguard = BodyguardAnt()
        bodyguard.action(gamestate) # Action without contained ant should not error

        # Bodyguard ant added before another ant
        bodyguard = BodyguardAnt()
        other_ant = ThrowerAnt()
        place = gamestate.places['tunnel_0_0']
        place.add_insect(bodyguard)  # Bodyguard in place first
        place.add_insect(other_ant)
        self.assertEqual(place.ant is bodyguard, True)
        self.assertEqual(bodyguard.ant_contained is other_ant, True)
      
    def test8_4(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
        
        # Bodyguard ant can be added after another ant
        bodyguard = BodyguardAnt()
        other_ant = ThrowerAnt()
        place = gamestate.places['tunnel_0_0']
        place.add_insect(other_ant)  # Other ant in place first
        self.assertEqual(place.ant is other_ant, True)
        place.add_insect(bodyguard)
        self.assertEqual(place.ant is bodyguard, True)
        self.assertEqual(bodyguard.ant_contained is other_ant, True)

    def test8_5(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing bodyguard performs thrower's action
        bodyguard = BodyguardAnt()
        thrower = ThrowerAnt()
        bee = Bee(2)
        # Place bodyguard before thrower
        gamestate.places["tunnel_0_0"].add_insect(bodyguard)
        gamestate.places["tunnel_0_0"].add_insect(thrower)
        gamestate.places["tunnel_0_3"].add_insect(bee)
        bodyguard.action(gamestate)
        self.assertEqual(bee.health, 1)

    def test8_6(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing bodyguard performs thrower's action
        bodyguard = BodyguardAnt()
        thrower = ThrowerAnt()
        bee = Bee(2)
        # Place thrower before bodyguard
        gamestate.places["tunnel_0_0"].add_insect(thrower)
        gamestate.places["tunnel_0_0"].add_insect(bodyguard)
        gamestate.places["tunnel_0_3"].add_insect(bee)
        bodyguard.action(gamestate)
        self.assertEqual(bee.health, 1)

    def test8_7(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing removing a bodyguard doesn't remove contained ant
        place = gamestate.places['tunnel_0_0']
        bodyguard = BodyguardAnt()
        test_ant = Ant(1)
        # add bodyguard first
        place.add_insect(bodyguard)
        place.add_insect(test_ant)
        gamestate.remove_ant('tunnel_0_0')
        self.assertEqual(place.ant is test_ant, True)
        self.assertEqual(bodyguard.place is None, True)

    def test8_8(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing bodyguarded ant keeps instance attributes
        test_ant = Ant()
        def new_action(gamestate):
            test_ant.health += 9000
        test_ant.action = new_action
        place = gamestate.places['tunnel_0_0']
        bodyguard = BodyguardAnt()
        place.add_insect(test_ant)
        place.add_insect(bodyguard)
        place.ant.action(gamestate)
        self.assertEqual(9001, place.ant.ant_contained.health)
      
    def test8_9(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing single BodyguardAnt cannot hold two other ants
        bodyguard = BodyguardAnt()
        first_ant = ThrowerAnt()
        place = gamestate.places['tunnel_0_0']
        place.add_insect(bodyguard)
        place.add_insect(first_ant)
        second_ant = ThrowerAnt()
        
        correct = False
        try:
            place.add_insect(second_ant)
        except (AssertionError):
            correct = True
        
        self.assertEqual(correct, True)
        
    def test8_10(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))


        # Testing BodyguardAnt cannot hold another BodyguardAnt
        bodyguard1 = BodyguardAnt()
        bodyguard2 = BodyguardAnt()
        place = gamestate.places['tunnel_0_0']
        place.add_insect(bodyguard1)
        
        correct = False
        try:
            place.add_insect(bodyguard2)
        except (AssertionError):
            correct = True
        
        self.assertEqual(correct, True)

    def test8_11(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # Testing BodyguardAnt takes all the damage
        thrower = ThrowerAnt()
        bodyguard = BodyguardAnt()
        bee = Bee(1)
        place = gamestate.places['tunnel_0_0']
        place.add_insect(thrower)
        place.add_insect(bodyguard)
        place.add_insect(bee)
        self.assertEqual(bodyguard.health, 2)

        bee.action(gamestate)
        self.assertEqual((bodyguard.health, thrower.health), (1, 1))
        bee.action(gamestate)
        self.assertEqual((bodyguard.health, thrower.health), (0, 1))

        self.assertEqual(bodyguard.place is None, True)
        self.assertEqual(place.ant is thrower, True)
        bee.action(gamestate)
        self.assertEqual(thrower.health, 0)
        self.assertEqual(place.ant is None, True)
      
    def test8_12(self):
        #setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

        # test proper call to death callback
        sys.stdout = io.StringIO()
        original_death_callback = Insect.death_callback
        Insect.death_callback = lambda x: print("insect died")
        place = gamestate.places["tunnel_0_0"]
        bee = Bee(3)
        bodyguard = BodyguardAnt()
        ant = ThrowerAnt()
        place.add_insect(bee)
        place.add_insect(ant)
        place.add_insect(bodyguard)
        bee.action(gamestate)
        bee.action(gamestate)
        self.assertEqual('insect died\n', sys.stdout.getvalue())
        sys.stdout = io.StringIO()
        bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
        self.assertEqual('insect died\n', sys.stdout.getvalue())
        Insect.death_callback = original_death_callback
    
    def test9_1(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing TankAnt parameters
        self.assertEqual(TankAnt.food_cost, 6)
        self.assertEqual(TankAnt.damage, 1)
        tank = TankAnt()
        self.assertEqual(tank.health, 2)

        # Testing TankAnt action
        tank = TankAnt()
        place = gamestate.places['tunnel_0_1']
        other_place = gamestate.places['tunnel_0_2']
        place.add_insect(tank)
        for _ in range(3):
            place.add_insect(Bee(3))
        other_place.add_insect(Bee(3))
        tank.action(gamestate)
        self.assertEqual(
            [bee.health for bee in place.bees], 
            [2, 2, 2]
        )
        self.assertEqual(
            [bee.health for bee in other_place.bees],
            [3]
        )

    def test9_2(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing TankAnt container methods
        tank = TankAnt()
        thrower = ThrowerAnt()
        place = gamestate.places['tunnel_0_1']
        place.add_insect(thrower)
        place.add_insect(tank)
        self.assertEqual(place.ant is tank, True)
        bee = Bee(3)
        place.add_insect(bee)
        tank.action(gamestate)   # Both ants attack bee
        self.assertEqual(bee.health, 1)
    
    def test9_3(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing TankAnt action
        tank = TankAnt()
        place = gamestate.places['tunnel_0_1']
        place.add_insect(tank)
        for _ in range(3):  # Add three bees with 1 health each
            place.add_insect(Bee(1))
        tank.action(gamestate)
        self.assertEqual(len(place.bees), 0)  # Bees removed from places because of TankAnt damage

    def test9_4(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing TankAnt.damage
        tank = TankAnt()
        tank.damage = 100
        place = gamestate.places['tunnel_0_1']
        place.add_insect(tank)
        for _ in range(3):
            place.add_insect(Bee(100))
        tank.action(gamestate)
        self.assertEqual(len(place.bees), 0)
        
    def test9_5(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Placement of ants
        tank = TankAnt()
        harvester = HarvesterAnt()
        place = gamestate.places['tunnel_0_0']
        # Add tank before harvester
        place.add_insect(tank)
        place.add_insect(harvester)
        gamestate.food = 0
        tank.action(gamestate)
        self.assertEqual(gamestate.food, 1)
      
        correct = False
        try:
            place.add_insect(TankAnt())
        except AssertionError:
            correct = True
        self.assertEqual(correct, True)

        self.assertEqual(place.ant is tank, True)
        self.assertEqual(tank.ant_contained is harvester, True)

        correct = False
        try:
            place.add_insect(HarvesterAnt())
        except AssertionError:
            correct = True
        self.assertEqual(correct, True)
        
        self.assertEqual(place.ant is tank, True)
        self.assertEqual(tank.ant_contained is harvester, True)

    def test9_6(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Placement of ants
        tank = TankAnt()
        harvester = HarvesterAnt()
        place = gamestate.places['tunnel_0_0']
        # Add harvester before tank
        place.add_insect(harvester)
        place.add_insect(tank)
        gamestate.food = 0
        tank.action(gamestate)
        self.assertEqual(gamestate.food, 1)

        correct = False
        try:
            place.add_insect(TankAnt())
        except AssertionError:
            correct = True
        self.assertEqual(correct, True)

        self.assertEqual(place.ant is tank, True)
        self.assertEqual(tank.ant_contained is harvester, True)

        correct = False
        try:
            place.add_insect(HarvesterAnt())
        except AssertionError:
            correct = True
        self.assertEqual(correct, True)

        self.assertEqual(place.ant is tank, True)
        self.assertEqual(tank.ant_contained is harvester, True)

    def test9_7(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        
        # Removing ants
        tank = TankAnt()
        test_ant = Ant()
        place = Place('Test')
        place.add_insect(tank)
        place.add_insect(test_ant)
        place.remove_insect(test_ant)
        self.assertEqual(tank.ant_contained is None, True)
        self.assertEqual(test_ant.place is None, True)
        place.remove_insect(tank)
        self.assertEqual(place.ant is None, True)
        self.assertEqual(tank.place is None, True)

        tank = TankAnt()
        place = Place('Test')
        place.add_insect(tank)
        tank.action(gamestate) # Action without ant_contained should not error

    def test9_8(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        
        # test proper call to death callback
        original_death_callback = Insect.death_callback
        Insect.death_callback = lambda x: print("insect died")
        place = gamestate.places["tunnel_0_0"]
        bee = Bee(3)
        tank = TankAnt()
        ant = ThrowerAnt()
        place.add_insect(bee)
        place.add_insect(ant)
        place.add_insect(tank)
        bee.action(gamestate)
        sys.stdout = io.StringIO()
        bee.action(gamestate)
        self.assertEqual('insect died\n', sys.stdout.getvalue())
        
        sys.stdout = io.StringIO()
        bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
        self.assertEqual('insect died\n', sys.stdout.getvalue())
        Insect.death_callback = original_death_callback

    def test10_1(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing water with Ants
        test_water = Water('Water Test1')
        ant = HarvesterAnt()
        test_water.add_insect(ant)
        self.assertEqual((ant.health, test_water.ant is None), (0, True))
        ant = Ant()
        test_water.add_insect(ant)
        self.assertEqual((ant.health, test_water.ant is None), (0, True))
        ant = ThrowerAnt()
        test_water.add_insect(ant)
        self.assertEqual((ant.health, test_water.ant is None), (0, True))

    def test10_2(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing water with soggy (non-waterproof) bees
        test_bee = Bee(1000000)
        test_bee.is_waterproof = False    # Make Bee non-waterproof
        test_water = Water('Water Test2')
        test_water.add_insect(test_bee)
        self.assertEqual(test_bee.health, 0)
        self.assertEqual(test_water.bees, [])

    def test10_3(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing water with waterproof bees
        test_bee = Bee(1)
        test_water = Water('Water Test3')
        test_water.add_insect(test_bee)
        self.assertEqual(test_bee.health, 1)
        self.assertEqual(test_bee in test_water.bees, True)

    def test10_4(self):
        # setup
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # test proper call to death callback
        original_death_callback = Insect.death_callback
        Insect.death_callback = lambda x: print("insect died")
        place = Water('Water Test4')
        soggy_bee = Bee(1)
        soggy_bee.is_waterproof = False
        sys.stdout = io.StringIO()
        place.add_insect(soggy_bee)
        self.assertEqual(sys.stdout.getvalue(), 'insect died\n')

        sys.stdout = io.StringIO()
        place.add_insect(Bee(1))
        place.add_insect(ThrowerAnt())
        self.assertEqual(sys.stdout.getvalue(), 'insect died\n')
        Insect.death_callback = original_death_callback
    

    def test10_5(self):
        beehive, layout = Hive(make_test_assault_plan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        old_add_insect = Place.add_insect

        # Testing water inheritance
        def new_add_insect(self = None, insect = None):
            if self == None:
                return
            print("called add_insect")
            old_add_insect(self, insect)

        Place.add_insect = new_add_insect
        test_bee = Bee(1)
        test_water = Water('Water Test4')
        sys.stdout = io.StringIO()
        test_water.add_insect(test_bee) # if this fails you probably didn't call `add_insect`
        self.assertEqual(sys.stdout.getvalue(), 'called add_insect\n')
        Place.add_insect = old_add_insect            
        
    def test11_1(self):
        # Testing ScubaThrower parameters
        scuba = ScubaThrower()
        self.assertEqual(ScubaThrower.food_cost, 6)
        self.assertEqual(scuba.health, 1)

    def test11_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing if ScubaThrower is waterproof
        water = Water('Water')
        ant = ScubaThrower()
        water.add_insect(ant)
        self.assertEqual(ant.place is water, True)
        self.assertEqual(ant.health, 1)

    def test11_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing that ThrowerAnt is not waterproof
        water = Water('Water')
        ant = ThrowerAnt()
        water.add_insect(ant)
        self.assertEqual(ant.place is water, False)
        self.assertEqual(ant.health, 0)

    def test11_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing ScubaThrower on land
        place1 = gamestate.places["tunnel_0_0"]
        place2 = gamestate.places["tunnel_0_4"]
        ant = ScubaThrower()
        bee = Bee(3)
        place1.add_insect(ant)
        place2.add_insect(bee)
        ant.action(gamestate)
        self.assertEqual(bee.health, 2)  # ScubaThrower can throw on land

    def test11_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing ScubaThrower in the water
        water = Water("water")
        water.entrance = gamestate.places["tunnel_0_1"]
        target = gamestate.places["tunnel_0_4"]
        ant = ScubaThrower()
        bee = Bee(3)
        water.add_insect(ant)
        target.add_insect(bee)
        ant.action(gamestate)
        self.assertEqual(bee.health, 2)  # ScubaThrower can throw in water
                          
    def test11_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
        old_thrower_action = ThrowerAnt.action
        old_throw_at = ThrowerAnt.throw_at

        # Testing ScubaThrower Inheritance from ThrowerAnt
        def new_action(self = None, gamestate = None):
            if self == None:
                return
            raise NotImplementedError()
        
        def new_throw_at(self = None, target = None):
            if self == None:
                return
            raise NotImplementedError()
        ThrowerAnt.action = new_action
        test_scuba = ScubaThrower()
        sys.stdout = io.StringIO()
        try:
            test_scuba.action(gamestate)
        except NotImplementedError:
            print('inherits action!')
        self.assertEqual('inherits action!\n', sys.stdout.getvalue())

        ThrowerAnt.action = old_thrower_action
        ThrowerAnt.throw_at = new_throw_at
        test_scuba = ScubaThrower()
        sys.stdout = io.StringIO()
        try:
            test_scuba.throw_at(Bee(1))
        except NotImplementedError:
            print('inherits throw_at!')
        self.assertEqual('inherits throw_at!\n', sys.stdout.getvalue())

        # tear down
        ThrowerAnt.action = old_thrower_action
        ThrowerAnt.throw_at = old_throw_at

    def test11_7(self):
        self.assertEqual(ScubaThrower.implemented, True)

    def test12_1(self):
        beehive = Hive(AssaultPlan())
        dimensions = (2, 9)
        gamestate = GameState(None, beehive, ant_types(), dry_layout, dimensions, food=100)

        # Testing QueenAnt parameters
        self.assertEqual(QueenAnt.food_cost, 7)
        queen = QueenAnt()
        self.assertEqual(queen.health, 1)

        # Abstraction tests
        original = ScubaThrower.construct
        ScubaThrower.__init__ = lambda self, health=2: print("scuba init")
        
        def modified_construct(cls=None, gamestate=None):
           if cls == None:
               return
           print("scuba construct")
           return super(ScubaThrower, cls).construct(gamestate)
        
        ScubaThrower.construct = classmethod(modified_construct)
        sys.stdout = io.StringIO()
        queen = QueenAnt.construct(gamestate)
        self.assertEqual('scuba construct\nscuba init\n', sys.stdout.getvalue())
        ScubaThrower.construct = original
        queen = QueenAnt.construct(gamestate)

    def test12_2(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), 
                                   ants.dry_layout, dimensions, food=20)
        ants.ants_lose = lambda: None

        # QueenAnt Placement
        queen = ants.QueenAnt.construct(gamestate)
        impostor = ants.QueenAnt.construct(gamestate)
        self.assertEqual(impostor is None, True) # you cannot create a second QueenAnt!
        front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
        tunnel = [gamestate.places['tunnel_0_{0}'.format(i)] for i in range(9)]
        tunnel[1].add_insect(back_ant)
        tunnel[7].add_insect(front_ant)
        self.assertEqual(tunnel[4].ant is None, True)
        self.assertEqual(back_ant.damage, 1)           # Ants should not be buffed
        self.assertEqual(front_ant.damage, 1)
        tunnel[4].add_insect(queen)
        queen.action(gamestate)
        self.assertEqual(1, queen.health)               # Long live the Queen!
        self.assertEqual(back_ant.damage, 2)           # Ants behind queen should be buffed
        self.assertEqual(front_ant.damage, 1)

    def test12_3(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), 
                                   ants.dry_layout, dimensions, food=20)
        ants.ants_lose = lambda: None

        # QueenAnt Removal
        queen = ants.QueenAnt.construct(gamestate)
        place = gamestate.places['tunnel_0_2']
        place.add_insect(queen)
        place.remove_insect(queen)
        self.assertEqual(place.ant is queen, True)        # True queen cannot be removed

    def test12_4(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), 
                                   ants.dry_layout, dimensions, food=20)
        ants.ants_lose = lambda: None

    def test12_5(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), 
                                   ants.dry_layout, dimensions, food=20)
        ants.ants_lose = lambda: None

        # QueenAnt knows how to swim
        queen = ants.QueenAnt.construct(gamestate)
        water = ants.Water('Water')
        water.add_insect(queen)
        self.assertEqual(queen.health, 1)

    def test12_5_2(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), 
                                   ants.dry_layout, dimensions, food=20)
        ants.ants_lose = lambda: None

        # Testing damage multiplier
        queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
        # layout
        # queen_tunnel: [Back, Guard/Guarded, Queen, Front, Bee     ]
        # side_tunnel : [Side,              ,      ,      , Side Bee]
        queen = ants.QueenAnt.construct(gamestate)
        back = ants.ThrowerAnt()
        front = ants.ThrowerAnt()
        guard = ants.BodyguardAnt()
        guarded = ants.ThrowerAnt()
        side = ants.ThrowerAnt()
        bee = ants.Bee(10)
        side_bee = ants.Bee(10)
        queen_tunnel[0].add_insect(back)
        queen_tunnel[1].add_insect(guard)
        queen_tunnel[1].add_insect(guarded)
        queen_tunnel[2].add_insect(queen)
        queen_tunnel[3].add_insect(front)
        side_tunnel[0].add_insect(side)
        queen_tunnel[4].add_insect(bee)
        side_tunnel[4].add_insect(side_bee)
        queen.action(gamestate)
        self.assertEqual(bee.health, 9)
        back.action(gamestate)
        self.assertEqual(bee.health, 7)
        front.action(gamestate)
        self.assertEqual(bee.health, 6)
        guard.action(gamestate)
        self.assertEqual(bee.health, 4) # if this is 5 you probably forgot to buff the contents of guard
        side.action(gamestate)
        self.assertEqual(side_bee.health, 9)

    def test12_6(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # Testing game over
        queen = ants.QueenAnt.construct(gamestate)
        tunnel = [gamestate.places['tunnel_0_{0}'.format(i)] for i in range(9)]
        tunnel[4].add_insect(queen)
        bee = ants.Bee(3)
        tunnel[6].add_insect(bee)     # Bee in a different place from the queen
        bee.action(gamestate)         # Game should not end
        bee.move_to(tunnel[4])        # Bee moved to place with queen
        
        correct = False
        try:
            bee.action(gamestate)         # Game should end
        except ants.AntsLoseException:
            # sys.stderr.write("Here")
            correct = True
        self.assertEqual(correct, True)
          
    def test(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # Testing if queen will not crash with no one to buff
        queen = ants.QueenAnt.construct(gamestate)
        gamestate.places['tunnel_0_2'].add_insect(queen)
        queen.action(gamestate)
        # Attack a bee
        bee = ants.Bee(3)
        gamestate.places['tunnel_0_4'].add_insect(bee)
        queen.action(gamestate)
        self.assertEqual(bee.health, 2) # Queen should still hit the bee
        
    def test12_8(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # Testing QueenAnt action method
        queen = ants.QueenAnt.construct(gamestate)
        bee = ants.Bee(10)
        ant = ants.ThrowerAnt()
        gamestate.places['tunnel_0_0'].add_insect(ant)
        gamestate.places['tunnel_0_1'].add_insect(queen)
        gamestate.places['tunnel_0_4'].add_insect(bee)
        queen.action(gamestate)
        self.assertEqual(bee.health, 9)   # Queen should damage bee
        self.assertEqual(ant.damage, 2)  # Queen should double damage
        ant.action(gamestate)
        self.assertEqual(bee.health, 7)   # If failed, ThrowerAnt has incorrect damage
        self.assertEqual(queen.health, 1)   # Long live the Queen

    def test12_9(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # Extensive damage doubling tests
        queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
        queen = ants.QueenAnt.construct(gamestate)
        queen_tunnel[7].add_insect(queen)
        # Turn 0
        thrower = ants.ThrowerAnt()
        fire = ants.FireAnt()
        side = ants.ThrowerAnt()
        front = ants.ThrowerAnt()
        queen_tunnel[0].add_insect(thrower)
        queen_tunnel[1].add_insect(fire)
        queen_tunnel[8].add_insect(front)
        side_tunnel[0].add_insect(side)
        # layout right now
        # [thrower, fire, , , , , , queen, front]
        # [side   ,     , , , , , ,      ,      ]
        thrower.damage, fire.damage = 101, 102
        front.damage, side.damage = 104, 105
        queen.action(gamestate)
        self.assertEqual((thrower.damage, fire.damage), (202, 204))
        self.assertEqual((front.damage, side.damage), (104, 105))
        # Turn 1
        tank = ants.TankAnt()
        guard = ants.BodyguardAnt()
        queen_tank = ants.TankAnt()
        queen_tunnel[6].add_insect(tank)          # Not protecting an ant
        queen_tunnel[1].add_insect(guard)         # Guarding FireAnt
        queen_tunnel[7].add_insect(queen_tank)    # Guarding QueenAnt
        # layout right now
        # [thrower, guard/fire, , , , , tank, queen_tank/queen, front]
        # [side   ,           , , , , ,     ,                 ,      ]
        tank.damage, guard.damage, queen_tank.damage = 1001, 1002, 1003
        queen.action(gamestate)
        # unchanged
        self.assertEqual((thrower.damage, fire.damage), (202, 204))
        self.assertEqual((front.damage, side.damage), (104, 105))
        self.assertEqual((tank.damage, guard.damage), (2002, 2004))
        self.assertEqual(queen_tank.damage, 1003)
        # Turn 2
        thrower1 = ants.ThrowerAnt()
        thrower2 = ants.ThrowerAnt()
        queen_tunnel[6].add_insect(thrower1)      # Add thrower1 in TankAnt
        queen_tunnel[5].add_insect(thrower2)
        # layout right now
        # [thrower, guard/fire, , , , thrower2, tank/thrower1, queen_tank/queen, front]
        # [side   ,           , , , ,         ,              ,                 ,      ]
        thrower1.damage, thrower2.damage = 10001, 10002
        queen.action(gamestate)
        self.assertEqual((thrower.damage, fire.damage), (202, 204))
        self.assertEqual((front.damage, side.damage), (104, 105))
        self.assertEqual((tank.damage, guard.damage), (2002, 2004))
        self.assertEqual(queen_tank.damage, 1003)
        self.assertEqual((thrower1.damage, thrower2.damage), (20002, 20004))
        # Turn 3
        tank.reduce_health(tank.health)             # Expose thrower1
        queen.action(gamestate)
        self.assertEqual((thrower.damage, fire.damage), (202, 204))
        self.assertEqual((front.damage, side.damage), (104, 105))
        self.assertEqual(guard.damage, 2004)
        self.assertEqual(queen_tank.damage, 1003)
        self.assertEqual((thrower1.damage, thrower2.damage), (20002, 20004))

    def test12_10(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # Adding/Removing QueenAnt with Container
        place = gamestate.places['tunnel_0_3']
        queen = ants.QueenAnt.construct(gamestate)
        container = ants.TankAnt()
        place.add_insect(container)

        self.assertEqual(place.ant is container, True)
        self.assertEqual(container.place is place, True)
        self.assertEqual(container.ant_contained is None, True)
                         
        place.add_insect(queen)
        place.remove_insect(queen)

        self.assertEqual(container.ant_contained is queen, True)
        self.assertEqual(queen.place is place, True)
        queen.action(gamestate) # should not error

    def test12_11(self):
        # setup
        importlib.reload(ants)
        beehive = ants.Hive(ants.AssaultPlan())
        dimensions = (2, 9)
        gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

        # test proper call to death callback
        original_death_callback = ants.Insect.death_callback
        ants.Insect.death_callback = lambda x: print("insect died")
        real = ants.QueenAnt.construct(gamestate)
        gamestate.places['tunnel_0_2'].add_insect(real)
        ants.Insect.death_callback = original_death_callback

    def test12_12(self):
        self.assertEqual(QueenAnt.implemented, True)

    def testEC_1(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing status parameters
        slow = SlowThrower()
        scary = ScaryThrower()
        self.assertEqual(SlowThrower.food_cost, 4)
        self.assertEqual(ScaryThrower.food_cost, 6)
        self.assertEqual(slow.health, 1)
        self.assertEqual(scary.health, 1)

    def testEC_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing Slow
        slow = SlowThrower()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(slow)
        gamestate.places["tunnel_0_4"].add_insect(bee)
        slow.action(gamestate)
        gamestate.time = 1
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_4') # SlowThrower should cause slowness on odd turns
          
        gamestate.time += 1
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_3') # SlowThrower should cause slowness on odd turns
          
        for _ in range(3):
            gamestate.time += 1
            bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_1')

    def testEC_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing Scare
        scary = ScaryThrower()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scary)
        gamestate.places["tunnel_0_4"].add_insect(bee)
        scary.action(gamestate)
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_5') # ScaryThrower should scare for two turns
          
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_6') # ScaryThrower should scare for two turns
          
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_5')

    def testEC_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Scary stings an ant
        scary = ScaryThrower()
        harvester = HarvesterAnt()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scary)
        gamestate.places["tunnel_0_4"].add_insect(bee)
        gamestate.places["tunnel_0_5"].add_insect(harvester)
        scary.action(gamestate)
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_5') # ScaryThrower should scare for two turns
          
        self.assertEqual(harvester.health, 1)
        bee.action(gamestate)
        self.assertEqual(harvester.health, 0)

    def testEC_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing if statuses stack
        slow = SlowThrower()
        bee = Bee(3)
        slow_place = gamestate.places["tunnel_0_0"]
        bee_place = gamestate.places["tunnel_0_8"]
        slow_place.add_insect(slow)
        bee_place.add_insect(bee)
        slow.action(gamestate)    # slow bee two times
        slow.action(gamestate)
        gamestate.time = 1
        bee.action(gamestate) # do nothing. There are 5 turns left with the bee slowed.
        self.assertEqual(bee.place.name, 'tunnel_0_8')
        gamestate.time = 2
        bee.action(gamestate) # moves forward. There are 4 turns left with the bee slowed.
        self.assertEqual(bee.place.name, 'tunnel_0_7')
        gamestate.time = 3
        bee.action(gamestate) # do nothing. There are 3 turns left with the bee slowed.
        self.assertEqual(bee.place.name, 'tunnel_0_7')
        gamestate.time = 4
        bee.action(gamestate) # moves forward. There are 2 turns left with the bee slowed.
        self.assertEqual(bee.place.name, 'tunnel_0_6')
        gamestate.time = 5
        bee.action(gamestate) # does nothing. There is 1 turn left with the bee slowed.
        self.assertEqual(bee.place.name, 'tunnel_0_6')
        gamestate.time = 6      # moves forward. The slow status has now worn off
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_5')
        gamestate.time = 7      # slow status has worn off
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 8      # slow status has worn off
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_3')

    def testEC_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing multiple scared bees
        scare1 = ScaryThrower()
        scare2 = ScaryThrower()
        bee1 = Bee(3)
        bee2 = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scare1)
        gamestate.places["tunnel_0_1"].add_insect(bee1)
        gamestate.places["tunnel_0_4"].add_insect(scare2)
        gamestate.places["tunnel_0_5"].add_insect(bee2)
        scare1.action(gamestate)
        scare2.action(gamestate)
        bee1.action(gamestate)
        bee2.action(gamestate)
        self.assertEqual(bee1.place.name, 'tunnel_0_2')
        self.assertEqual(bee2.place.name, 'tunnel_0_6')
        bee1.action(gamestate)
        bee2.action(gamestate)
        self.assertEqual(bee1.place.name, 'tunnel_0_3')
        self.assertEqual(bee2.place.name, 'tunnel_0_7')
        bee1.action(gamestate)
        bee2.action(gamestate)
        self.assertEqual(bee1.place.name, 'tunnel_0_2')
        self.assertEqual(bee2.place.name, 'tunnel_0_6')

    def testEC_6_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        scare = ScaryThrower()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scare)
        gamestate.places["tunnel_0_1"].add_insect(bee)
        scare.action(gamestate)
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_2')
        bee.action(gamestate)
        self.assertEqual(bee.place.name, 'tunnel_0_3')
        #
        # Same bee should not be scared more than once
        scare.action(gamestate)
        bee.action(gamestate)
        bee.place.name

    def testEC_7(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing long status stack
        scary = ScaryThrower()
        slow = SlowThrower()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scary)
        gamestate.places["tunnel_0_1"].add_insect(slow)
        gamestate.places["tunnel_0_3"].add_insect(bee)
        scary.action(gamestate) # scare bee once
        gamestate.time = 0
        bee.action(gamestate) # scared
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        for _ in range(3): # slow bee three times, for a total of 9 turns
            slow.action(gamestate)
        gamestate.time = 1
        bee.action(gamestate) # scared, but also slowed for 9 more turns, so it doesn't move back yet
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 2
        bee.action(gamestate) # after this, no longer scared, but still slowed for 8 turns
        self.assertEqual(bee.place.name, 'tunnel_0_5') #  it's an even turn, so it can be scared and move backwards
          
        gamestate.time = 3
        bee.action(gamestate) # slowed for 7 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_5')
        gamestate.time = 4
        bee.action(gamestate) # slowed for 6 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 5
        bee.action(gamestate) # slowed for 5 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 6
        bee.action(gamestate) # slowed for 4 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_3')
        gamestate.time = 7
        bee.action(gamestate) # slowed for 3 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_3')
        gamestate.time = 8
        bee.action(gamestate) # slowed for 2 more turns
        self.assertEqual(bee.place.name, 'tunnel_0_2')
        gamestate.time = 9
        bee.action(gamestate) # last slowed turn
        self.assertEqual(bee.place.name, 'tunnel_0_2')
        gamestate.time = 10
        bee.action(gamestate) # no longer slowed
        self.assertEqual(bee.place.name, 'tunnel_0_1')

    def testEC_7_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        scary = ScaryThrower()
        slow = SlowThrower()
        bee = Bee(3)
        gamestate.places["tunnel_0_0"].add_insect(scary)
        gamestate.places["tunnel_0_1"].add_insect(slow)
        gamestate.places["tunnel_0_3"].add_insect(bee)
        slow.action(gamestate) # slow bee
        scary.action(gamestate) # scare bee
        self.assertEqual(bee.place.name, 'tunnel_0_3')
        gamestate.time = 0
        bee.action(gamestate) # scared and slowed - even game time, so *can* back away
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 1
        bee.action(gamestate) # scared and slowed - odd game time, so *cannot* back away
        self.assertEqual(bee.place.name, 'tunnel_0_4')
        gamestate.time = 2
        bee.action(gamestate) # scared and slowed - even game time, so *can* back away, no longer scared after this
        self.assertEqual(bee.place.name, 'tunnel_0_5')
        gamestate.time = 3
        bee.action(gamestate) # neither scared nor slowed
        self.assertEqual(bee.place.name, 'tunnel_0_4')

        self.assertEqual(ScaryThrower.implemented, True)
        self.assertEqual(SlowThrower.implemented, True)

    def testOP1_1(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing NinjaAnt parameters
        ninja = NinjaAnt()
        self.assertEqual(ninja.health, 1)
        self.assertEqual(NinjaAnt.food_cost, 5)
        # Testing blocks_path
        self.assertEqual(NinjaAnt.blocks_path, False)
        self.assertEqual(HungryAnt.blocks_path, True)
        self.assertEqual(FireAnt.blocks_path, True)

    def testOP1_2(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing NinjaAnts do not block bees
        p0 = gamestate.places["tunnel_0_0"]
        p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
        bee = Bee(2)
        ninja = NinjaAnt()
        thrower = ThrowerAnt()
        p0.add_insect(thrower)            # Add ThrowerAnt to p0
        p1.add_insect(bee)
        p1.add_insect(ninja)              # Add the Bee and NinjaAnt to p1
        bee.action(gamestate)
        self.assertEqual(bee.place is ninja.place, False)          # Did NinjaAnt block the Bee from moving?
        self.assertEqual(bee.place is p0, True)
        self.assertEqual(ninja.health, 1)
        bee.action(gamestate)
        self.assertEqual(bee.place is p0, True)                   # Did ThrowerAnt block the Bee from moving?

    def testOP1_3(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing non-blocking ants do not block bees
        p0 = gamestate.places["tunnel_0_0"]
        p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
        bee = Bee(2)
        ninja_fire = FireAnt(1)
        ninja_fire.blocks_path = False
        thrower = ThrowerAnt()
        p0.add_insect(thrower)            # Add ThrowerAnt to p0
        p1.add_insect(bee)
        p1.add_insect(ninja_fire)              # Add the Bee and NinjaAnt to p1
        bee.action(gamestate)
        self.assertEqual(bee.place is ninja_fire.place, False) # Did the "ninjaish" FireAnt block the Bee from moving?
        self.assertEqual(bee.place is p0, True)
        self.assertEqual(ninja_fire.health, 1)
        bee.action(gamestate)
        self.assertEqual(bee.place is p0, True) # Did ThrowerAnt block the Bee from moving?

    def testOP1_4(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing NinjaAnt strikes all bees in its place
        test_place = gamestate.places["tunnel_0_0"]
        for _ in range(3):
            test_place.add_insect(Bee(2))
        ninja = NinjaAnt()
        test_place.add_insect(ninja)
        ninja.action(gamestate)   # should strike all bees in place
        self.assertEqual([bee.health for bee in test_place.bees], [1, 1, 1])
        
    def testOP1_5(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing NinjaAnt doesn't hardcode damage
        test_place = gamestate.places["tunnel_0_0"]
        for _ in range(3):
            test_place.add_insect(Bee(100))
        ninja = NinjaAnt()
        ninja.damage = 50
        test_place.add_insect(ninja)
        ninja.action(gamestate)   # should strike all bees in place
        self.assertEqual([bee.health for bee in test_place.bees], [50, 50, 50])

    def testOP1_6(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing NinjaAnt strikes all bees, even if some expire
        test_place = gamestate.places["tunnel_0_0"]
        for _ in range(3):
            test_place.add_insect(Bee(1))
        ninja = NinjaAnt()
        test_place.add_insect(ninja)
        ninja.action(gamestate)   # should strike all bees in place
        self.assertEqual(len(test_place.bees), 0)

    def testOP1_7(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing damage is looked up on the instance
        place = gamestate.places["tunnel_0_0"]
        bee = Bee(900)
        place.add_insect(bee)
        buffNinja = NinjaAnt()
        buffNinja.damage = 500  # Sharpen the sword
        place.add_insect(buffNinja)
        buffNinja.action(gamestate)
        self.assertEqual(bee.health, 400)

    def testOP1_8(self):
        # setup
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        # Testing Ninja ant does not crash when left alone
        ninja = NinjaAnt()
        gamestate.places["tunnel_0_0"].add_insect(ninja)
        ninja.action(gamestate)

        # Testing Bee does not crash when left alone
        bee = Bee(3)
        gamestate.places["tunnel_0_1"].add_insect(bee)
        bee.action(gamestate)

    def testOP1_9(self):
        self.assertEqual(NinjaAnt.implemented, True)

    def testOP2_1(self):
        beehive, layout = Hive(AssaultPlan()), dry_layout
        dimensions = (1, 9)
        gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

        laser = LaserAnt()
        ant = HarvesterAnt(2)
        bee1 = Bee(2)
        bee2 = Bee(2)
        bee3 = Bee(2)
        bee4 = Bee(2)
        gamestate.places["tunnel_0_0"].add_insect(laser)
        gamestate.places["tunnel_0_0"].add_insect(bee4)
        gamestate.places["tunnel_0_3"].add_insect(bee1)
        gamestate.places["tunnel_0_3"].add_insect(bee2)
        gamestate.places["tunnel_0_4"].add_insect(ant)
        gamestate.places["tunnel_0_5"].add_insect(bee3)
        laser.action(gamestate)
        self.assertEqual(bee4.health, 0.0)
        self.assertEqual(bee1.health, 0.8125)
        self.assertEqual(bee2.health, 0.875)
        self.assertEqual(ant.health, 1.1875)
        self.assertEqual(bee3.health, 1.5)
        self.assertEqual(LaserAnt.implemented, True)
    
    def tearDown(self) -> None:
        # tear down
        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = self.old_throw_at
        return super().tearDown()