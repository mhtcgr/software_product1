package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.PyObject;

public abstract class Expression {
    protected PyObject val;
    public Expression(PyObject val){
        this.val = val;
    }
    public Expression(){}
    public abstract PyObject eval(ProgramState programState);
}
