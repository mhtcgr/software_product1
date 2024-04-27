package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.FunctionState;
import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.interpreter.statement.Statement;
import pers.xia.jpython.object.PyObject;
import pers.xia.jpython.object.PyVar;

import java.util.List;
import java.util.Stack;

public class FunctionCallExpression extends Expression {
    protected String functionName;
    protected List<Expression> parameterValue;

    public FunctionCallExpression(String functionName, List<Expression> parameterValue){
        this.functionName = functionName;
        this.parameterValue = parameterValue;
    }

    @Override
    public PyObject eval(ProgramState programState) {
        Stack<FunctionState> FunctionStateStack = programState.getFunctionStateStack();
        //1. FunctionObj 压入栈
        FunctionState functionState = new FunctionState();
        //2. 创建一个新的ProgramState 实例对象，更新变量
        List<Statement> functionStatements = programState.getFunctionStatements(this.functionName);
        List<String> parameterNames = programState.getParameterNames(this.functionName);

        //2.2 遍历 parameterValue 获取入参数值。
        for (int i = 0; i < this.parameterValue.size(); i++) {
            Expression param = this.parameterValue.get(i);
            PyObject val =  param.eval(programState);
            if(val instanceof PyVar){
                val = programState.getVariable(((PyVar) val).getVarName());
            }
            String valName = parameterNames.get(i);
            functionState.updateVariable(valName,val);
        }
        FunctionStateStack.push(functionState);
        for (Statement functionStatement : functionStatements) {
            //2.3在returnExpression 中更新 返回值
            functionStatement.run(programState);
            if(FunctionStateStack.peek().hasReturnValue()){
                break;
            }
        }
        //3. 按顺序出栈FuncStack，获取返回值。
        return FunctionStateStack.pop().getReturnValue();
    }
}
