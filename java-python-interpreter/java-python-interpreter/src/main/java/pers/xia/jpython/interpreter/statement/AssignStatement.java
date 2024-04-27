package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;
import pers.xia.jpython.object.PyObject;

public class AssignStatement implements Statement {
    private String[] variableName;
    private Expression expression;

    public AssignStatement(String[] variableName, Expression expression) {
        this.variableName = variableName;
        this.expression = expression;
    }


    @Override
    public void run(ProgramState programState) {
        PyObject expressionValue = expression.eval(programState);
        for(String vn:variableName) {
            programState.setVariable(vn, expressionValue);
        }
    }
}
