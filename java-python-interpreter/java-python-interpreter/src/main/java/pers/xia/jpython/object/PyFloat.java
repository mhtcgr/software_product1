package pers.xia.jpython.object;

public class PyFloat extends PyObject
{
    double num;

    public PyFloat(double num)
    {
        this.num = num;
    }

    public PyFloat(String s){
        this.num = Double.parseDouble(s);
    }
    public double asFloat(){
        return  num;
    }

    @Override
    public String toString() {
        return String.valueOf(num);
    }

    @Override
    public boolean equals(PyObject p) {
        if(p instanceof PyLong || p instanceof PyFloat || p instanceof PyBoolean){
            return !this.sub(p).asBoolean();
        }
        return false;
    }

    @Override
    public boolean asBoolean() {
        return this.num != 0;
    }

    @Override
    public PyObject add(PyObject p) {
        if (p instanceof PyLong){
            return new PyFloat(this.num + ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num+((PyFloat) p).asFloat());
        }
        if (p instanceof PyUnicode){
            return new PyUnicode( (this.toString() + p.toString()).getBytes(), "utf-8");
        }
        if(p instanceof PyBoolean){
            return new PyFloat(this.num+((PyBoolean) p).asInt());
        }
        else{
            super.add(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject sub(PyObject p) {
        if (p instanceof PyLong){
            return new PyFloat(this.num - ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num - ((PyFloat) p).asFloat());
        }
        if(p instanceof PyBoolean){
            return new PyFloat(this.num - ((PyBoolean) p).asInt());
        }
        else{
            super.add(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject mul(PyObject p) {
        if (p instanceof PyLong){
            return new PyFloat(this.num * ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num * ((PyFloat) p).asFloat());
        }
        if(p instanceof PyBoolean){
            return new PyFloat(this.num * ((PyBoolean) p).asInt());
        }
        else{
            super.add(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject uSub() {
        return new PyFloat(-this.num);
    }

    @Override
    public String getType(){
        return "num";
    }
}
