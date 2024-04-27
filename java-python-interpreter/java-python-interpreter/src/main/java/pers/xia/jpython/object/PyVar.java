package pers.xia.jpython.object;

public class PyVar extends PyObject{
    private String varName;

    public PyVar(String varName) {
        this.varName = varName;
    }

    public String getVarName() {
        return varName;
    }

    @Override
    public String toString(){
        return varName;
    }
}
