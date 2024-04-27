package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.expression.Expression;

import java.util.ArrayList;
import java.util.List;

// Todo: 修改BlockStatement实现不同步长
public abstract class BlockStatement implements Statement{
    private Expression expression;
    private List<Statement> body;
    private List<Statement> elseBody;


    public BlockStatement(Expression expression, List<Statement> body) {
        this.expression = expression;
        this.body = body;
        this.elseBody = new ArrayList<>();
    }

    public BlockStatement(Expression expression, List<Statement> body, List<Statement> elseBody) {
        this.expression = expression;
        this.body = body;
        this.elseBody = elseBody;
    }

    public void ifBlock(ProgramState programState) {
        boolean res = (expression.eval(programState)).asBoolean();
        if(res){
            bodyBlock(programState);
        }else{
            elseBlock(programState);
        }
    }

    public void whileLoop(ProgramState programState) {
        // TODO: 完成whileLoop实现while循环
    }

    // 返回值为true则表示该block有需要向外传递的break
    public boolean bodyBlock(ProgramState programState) {
        for (Statement statement: body){
            // body里面有break和continue的话，需要将当前if语句的breakFlag或continueFlag进行相应的修改
            if(statement instanceof BreakStatement){
                if(this instanceof IfStatement){
                    ((IfStatement) this).breakFlag = true;
                }
                return true;
            }else if(statement instanceof ContinueStatement){
                if(this instanceof IfStatement){
                    ((IfStatement) this).continueFlag = true;
                }
                return false;
            }
            //run之后 如果是ifStatement,其flag可能会发生改变，所以需要判断是否跳出
            statement.run(programState);
            if (statement instanceof IfStatement){
                if(((IfStatement) statement).breakFlag) return true;
                if(((IfStatement) statement).continueFlag) {
                    // 重置continueFlag 以免影响下次循环判断
                    ((IfStatement) statement).continueFlag = false;
                    return false;
                };
            }
        }
        return false;
    }

    // 返回值表示该block是否有需要向外传递的break
    public boolean elseBlock(ProgramState programState) {
        for (Statement statement: elseBody){
            if(statement instanceof BreakStatement){
                if(this instanceof IfStatement){
                    ((IfStatement) this).breakFlag = true;
                }
                return true;
            }else if(statement instanceof ContinueStatement){
                if(this instanceof IfStatement){
                    ((IfStatement) this).continueFlag = true;
                }
                return false;
            }
            //run之后 如果是ifStatement,breakFlag可能会发生改变，所以需要判断是否跳出
            statement.run(programState);
            if (statement instanceof IfStatement){
                if(((IfStatement) statement).breakFlag) return true;
                if(((IfStatement) statement).continueFlag) {
                    // 重置continueFlag 以免影响下次循环判断
                    ((IfStatement) statement).continueFlag = false;
                    return false;
                };
            }
        }
        return false;
    }

}
