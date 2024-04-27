package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;

public class ExprStatement implements Statement {
    private Expression expression;

    public ExprStatement(Expression expression) {
        this.expression = expression;
    }

    @Override
    public void run(ProgramState programState) {
        if(expression.eval(programState)!=null){
            System.out.println(expression.eval(programState));
        }
    }
}
