package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.PyObject;

public class ConstantExpression extends Expression{

    public ConstantExpression(PyObject n) {
        super(n);
    }

    @Override
    public PyObject eval(ProgramState programState) {
        return this.val;
    }
}
