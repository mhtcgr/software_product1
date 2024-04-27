package pers.xia.jpython.object;

public class PyString extends PyObject{
    private String str;

    public PyString(String str) {
        this.str = str;
    }
    public String getVal(){
        return str;
    }

    @Override
    public String toString() {
        return str;
    }
//    @Override
//    public PyObjType getType() {
//        return PyObjType.PyStringType;
//    }
}
