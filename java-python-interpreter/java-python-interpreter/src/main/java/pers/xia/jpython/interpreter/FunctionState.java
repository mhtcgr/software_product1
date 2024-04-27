package pers.xia.jpython.interpreter;

import pers.xia.jpython.object.PyObject;

import java.util.HashMap;

public class FunctionState extends ProgramState {
    private HashMap<String, PyObject> variableHeap;
    private PyObject returnVal;

    public FunctionState() {
        this.variableHeap = new HashMap<>();
    }

    public void updateVariable(String valName,PyObject pyObj){
        variableHeap.put(valName,pyObj);
    }
    public boolean hasReturnValue() {
        if(returnVal == null){
            return false;
        }
        return true;
    }
    public PyObject getReturnValue() {
        if(hasReturnValue() != true){
//            System.out.println("Does not have specified return value");
        }
        //return setReturnValue(); //was not able to figure it out
        return returnVal;
    }
    public void setReturnValue(PyObject returnValue) {
        this.returnVal =returnValue;
    }
    public PyObject getVariable(String variable) {
        if (!variableHeap.containsKey(variable)) {
            throw new RuntimeException("Undefined variable: " + variable);
        }
        return variableHeap.get(variable);

    }
    public boolean hasVariable(String variable) {
        return variableHeap.containsKey(variable);
    }
}
