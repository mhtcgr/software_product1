package pers.xia.jpython.object;

import java.util.Collections;

public class PyLong extends PyObject
{
    private long num;

    public PyLong(long num)
    {
        this.num = num;
    }

    public static PyObject newLong(String str)
    {
        if (str.length() <= 1)
        {
            return new PyLong(Long.parseLong((str)));
        }
        try
        {
            if (str.charAt(1) == 'x' || str.charAt(1) == 'X')
            {
                return new PyLong(Long.parseLong(str.substring(2), 16));
            }
            else if (str.charAt(1) == 'b' || str.charAt(1) == 'B')
            {
                return new PyLong(Long.parseLong(str.substring(2), 2));
            }
            else if (str.charAt(1) == 'o' || str.charAt(1) == 'O')
            {
                return new PyLong(Long.parseLong(str.substring(2), 8));
            }
            else
            {
                return new PyLong(Long.parseLong((str)));
            }
        }
        catch (NumberFormatException err)
        {
            //System.out.println(str);
            return new PyNumber(str);
        }
    }

    public long asLong()
    {
        return num;
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
            return new PyLong(this.num + ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num + ((PyFloat) p).asFloat());
        }
        if (p instanceof PyUnicode){
            return new PyUnicode( (this.toString() + p.toString()).getBytes(), "utf-8");
        }
        if(p instanceof PyBoolean){
            return new PyLong(this.num + ((PyBoolean) p).asInt());
        }
        else{
            super.add(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject sub(PyObject p) {
        if (p instanceof PyLong){
            return new PyLong(this.num - ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num - ((PyFloat) p).asFloat());
        }
        if(p instanceof PyBoolean){
            return new PyLong(this.num - ((PyBoolean) p).asInt());
        }
        else{
            super.sub(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject mul(PyObject p) {
        if (p instanceof PyLong){
            return new PyLong(this.num * ((PyLong) p).asLong());
        }
        if (p instanceof PyFloat){
            return new PyFloat(this.num * ((PyFloat) p).asFloat());
        }
        if(p instanceof PyBoolean){
            return new PyLong(this.num * ((PyBoolean) p).asInt());
        }
        if(p instanceof PyUnicode){
            return new PyUnicode(String.join("", Collections.nCopies((int) this.num, p.toString())).getBytes(),"utf-8");
        }
        else{
            super.mul(p);
            return new PyNone();
        }
    }

    @Override
    public PyObject uSub() {
        return new PyLong(-this.num);
    }

    @Override
    public String getType(){
        return "num";
    }
}
