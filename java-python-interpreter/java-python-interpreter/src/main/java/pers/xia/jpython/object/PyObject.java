package pers.xia.jpython.object;


public abstract class PyObject
{
//    public abstract PyObjType getType();
    public static PyObject objectToPyObj(Object obj){
        if (obj instanceof Long){
            return new PyLong((long)obj);
        }
        if(obj instanceof Double){
            return new PyFloat((double) obj);
        }
        if(obj instanceof String){
            return new PyUnicode( ((String) obj).getBytes(), "utf-8");
        }
        return new PyNone();
    }

    public boolean asBoolean(){
        return true;
    }

    public PyObject add(PyObject p){
        throw new PyExceptions(PyExceptions.ErrorType.TYPE_ERROR, "TypeError: unsupported operand type(s) for " + this.getType()+" and "+p.getType());
    }

    public PyObject sub(PyObject p){
        throw new PyExceptions(PyExceptions.ErrorType.TYPE_ERROR, "TypeError: unsupported operand type(s) for " + this.getType()+" and "+p.getType());
    }

    public PyObject mul(PyObject p){
        throw new PyExceptions(PyExceptions.ErrorType.TYPE_ERROR, "TypeError: unsupported operand type(s) for " + this.getType()+" and "+p.getType());
    }

    public PyObject uSub(){
        throw new PyExceptions(PyExceptions.ErrorType.TYPE_ERROR, "TypeError: unsupported operand type(s) for " + this.getType());
    }

    public boolean equals(PyObject p){
        return false;
    }

    public String getType(){
        return "object";
    }


}
