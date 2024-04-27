package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.PyObject;

public class PrintStatement implements Statement {
    public PrintStatement() {
    }
    //the varName in VariableHeap.
    private static final String varName = "arg";
    @Override
    public void run(ProgramState programState) {
        PyObject variable = programState.getVariable(varName);
        printPy(variable);
    }
    public void printPy(PyObject object){
        System.out.println(object.toString());
    }
}
