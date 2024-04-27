package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;

import java.util.List;

public class IfStatement extends BlockStatement {
    // 只有if块的break,continue需要向外层传递
    protected boolean breakFlag = false;
    protected boolean continueFlag = false;


    public IfStatement(Expression expression, List<Statement> body, List<Statement> elseBody) {
        super(expression, body, elseBody);
    }

    @Override
    public void run(ProgramState programState) {
        ifBlock(programState);
    }
}
