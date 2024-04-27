package pers.xia.jpython.object;

public class PyBoolean extends PyObject
{
    boolean b;
    public PyBoolean(boolean b)
    {
        this.b = b;
    }

    @Override
    public boolean asBoolean(){
        return this.b;
    }
    @Override
    public String toString(){
        return b ? "True" : "False";
    }

    public int asInt() { return b ? 1 : 0;}

    @Override
    public boolean equals(PyObject p) {
        if(p instanceof PyLong || p instanceof PyFloat || p instanceof PyBoolean){
            return !this.sub(p).asBoolean();
        }
        return false;
    }

    @Override
    public PyObject add(PyObject p) {
        if(p instanceof PyFloat){
            return new PyFloat(this.asInt() + ((PyFloat) p).asFloat());
        }
        if(p instanceof PyLong){
            return new PyLong(this.asInt()+((PyLong) p).asLong());
        }
        if(p instanceof PyBoolean){
            return new PyLong(this.asInt()+((PyBoolean) p).asInt());
        }
        if(p instanceof PyUnicode){
            //经过试验不支持
        }
        super.add(p);
        return new PyNone();
    }

    @Override
    public PyObject sub(PyObject p) {
        if(p instanceof PyFloat){
            return new PyFloat(this.asInt() - ((PyFloat) p).asFloat());
        }
        if(p instanceof PyLong){
            return new PyLong(this.asInt() - ((PyLong) p).asLong());
        }
        if(p instanceof PyBoolean){
            return new PyLong(this.asInt() - ((PyBoolean) p).asInt());
        }
        return super.sub(p);
    }

    @Override
    public PyObject uSub() {
        return new PyLong(-this.asInt());
    }


    @Override
    public String getType(){
        return "bool";
    }
}
