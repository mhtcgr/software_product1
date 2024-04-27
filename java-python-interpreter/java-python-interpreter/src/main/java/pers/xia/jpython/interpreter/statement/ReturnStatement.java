package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.FunctionState;
import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;
import pers.xia.jpython.object.PyObject;

public class ReturnStatement implements Statement{
    Expression expression;

    public ReturnStatement(Expression expression) {
        this.expression = expression;
    }
    @Override
    public void run(ProgramState programState) {
        PyObject expressionValue = expression.eval(programState);
        FunctionState topFunctionState = programState.getTopFunctionState();
        topFunctionState.setReturnValue(expressionValue);
    }
}
