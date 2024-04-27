import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.AfterEach;
import pers.xia.jpython.ast.Module;
import pers.xia.jpython.grammar.GramInit;
import pers.xia.jpython.interpreter.Interpreter;
import pers.xia.jpython.object.PyExceptions;
import pers.xia.jpython.parser.Ast;
import pers.xia.jpython.parser.Node;
import pers.xia.jpython.parser.ParseToken;
import utils.AuthorAndTime;


import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.PrintStream;
import static org.junit.jupiter.api.Assertions.assertEquals;

@AuthorAndTime(author = "wangzhen",time = "2023/06/18")
public class InterperterTest {
    public static ByteArrayOutputStream outContent=null;
    public static Ast ast = null;

    private final PrintStream originalOut = System.out;
    static {
        // 捕获 stdout 并运行代码
        outContent= new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        ast = new Ast();
    }
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    private static void testCode(String fileName,String expectedOutput ){
        File file = new File(fileName);
        try
        {
            Node node = ParseToken.parseFile(file, GramInit.grammar, 1);
            Module mod = (Module) ast.fromNode(node);
            Interpreter interpreter = new Interpreter(mod.getBody());
            interpreter.runProgram();
            String printedOutput = outContent.toString().trim();
            System.out.println(printedOutput);
            // 检查输出是否正确
            assertEquals(expectedOutput, printedOutput);
        }
        catch (PyExceptions e)
        {
            System.out.println(fileName);
            e.printStackTrace();
            throw e;
        }
    }
    @AfterEach
    public void cleanUp() {
        // 恢复原始的 System.out 输出流
        System.setOut(originalOut);
        // 清空 outContent 的缓存内容
        outContent.reset();
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask1() {
        String fileName= "src/test/resources/InterpreterTask1.py";
        String expectedOutput="1\n1";
        testCode(fileName,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask2() {
        String fileName= "src/test/resources/InterpreterTask2.py";
        String expectedOutput="2.0\n"+"1\n"+"0\n"+"2";
        testCode(fileName,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask3() {
        String fileName= "src/test/resources/InterpreterTask3.py";
        String expectedOutput="0\n" +
                "2\n" +
                "4\n" +
                "6\n" +
                "8";
        testCode(fileName,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask4() {
        String fileName= "src/test/resources/InterpreterTask4.py";
        String expectedOutput="1\n" +
                "3\n" +
                "4";
        testCode(fileName,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask5() {
        String fileName= "src/test/resources/InterpreterTask5.py";
        String expectedOutput="and\nor";
        testCode(fileName,expectedOutput);
    }

    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void testTask6() {
        String fileName = "src/test/resources/InterpreterTask6.py";
        String expectedOutput="120\n2";
        testCode(fileName,expectedOutput);
    }



}
