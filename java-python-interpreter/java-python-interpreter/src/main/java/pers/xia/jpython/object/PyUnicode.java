package pers.xia.jpython.object;

import java.io.UnsupportedEncodingException;
import java.util.Collections;

import pers.xia.jpython.object.PyExceptions.ErrorType;

public class PyUnicode extends PyObject
{
    public String str;

    public PyUnicode(byte[] b, String encode)
    {
        try
        {
            this.str = new String(b, encode);
        }
        catch (UnsupportedEncodingException e)
        {
            e.printStackTrace();
            throw new PyExceptions(ErrorType.SYSTEM_ERROR,
                    "Can't convert bytes to str implicitly");
        }
    }

    public static PyUnicode internFromString(String str)
    {
        return internFromString(str, false);
    }

    public static PyUnicode internFromString(String str, boolean rawmode)
    {
        return new PyUnicode(str.substring(1,str.length()-1), rawmode);
    }

    private PyUnicode(String str, boolean rawmode)
    {
        this.str = str;
        if(!rawmode)
        {
            this.str.replace("\\n", "\n");
            this.str.replace("\\t", "\t");
            this.str.replace("\\\\", "\\");
        }
    }

    private PyUnicode(PyObject obj)
    {
    }

    public static PyUnicode concat(PyObject left, PyObject right)
    {
        if(!(left instanceof PyUnicode))
        {
            throw new PyExceptions(ErrorType.SYSTEM_ERROR, "transform error",
                    left);
        }

        return ((PyUnicode) left).concat(right);
    }

    public PyUnicode concat(PyObject obj)
    {
        if(!(obj instanceof PyUnicode))
        {
            throw new PyExceptions(ErrorType.SYSTEM_ERROR, "transform error",
                    obj);
        }

        String newStr = this.str + ((PyUnicode) obj).str;
        return internFromString(newStr);

    }

    @Override
    public String toString() {
        replaceEscapes();
        return str;
    }

    public void replaceEscapes() {
        str = str.replace("\\n", "\n");
        str = str.replace("\\t", "\t");
        str = str.replace("\\r", "\r");
        str = str.replace("\\b", "\b");
        str = str.replace("\\\"", "\"");
        str = str.replace("\\'", "'");
        str = str.replace("\\\\", "\\");
    }
    public int compare(PyUnicode str){
        return 0 - this.str.compareTo(str.str);
    }

    @Override
    public boolean asBoolean() {
        return !this.str.equals("");
    }

    @Override
    public PyObject add(PyObject p) {
        return new PyUnicode( (this.str + p.toString()).getBytes(), "utf-8");
    }

    @Override
    public PyObject mul(PyObject p) {
        if(p instanceof PyLong){
            return new PyUnicode(String.join("", Collections.nCopies((int) ((PyLong) p).asLong(), this.str)).getBytes(),"utf-8");
        }
        else{
            super.mul(p);
            return new PyNone();
        }
    }

    @Override
    public String getType(){
        return "str";
    }
}
