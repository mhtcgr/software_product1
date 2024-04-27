package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.PyObject;

public class VariableExpression extends Expression {

    public VariableExpression(PyObject val) {
        super(val);
    }

    @Override
    public PyObject eval(ProgramState programState) {
        return programState.getVariable(this.val.toString());
    }
}
