package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;

import java.util.List;

public class WhileStatement extends BlockStatement{

    public WhileStatement(Expression expression, List<Statement> body){
        super(expression, body);
    }
    public WhileStatement(Expression expression, List<Statement> body, List<Statement> elseBody) {
        super(expression, body, elseBody);
    }

    @Override
    public void run(ProgramState programState) {
        whileLoop(programState);
    }

}