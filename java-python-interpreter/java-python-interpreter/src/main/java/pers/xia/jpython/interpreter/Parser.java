package pers.xia.jpython.interpreter;

import pers.xia.jpython.ast.*;
import pers.xia.jpython.interpreter.expression.*;
import pers.xia.jpython.interpreter.expression.Expression;
import pers.xia.jpython.interpreter.statement.AssignStatement;
import pers.xia.jpython.interpreter.statement.Statement;
import pers.xia.jpython.object.*;

import java.util.ArrayList;
import java.util.List;

public class Parser {

    public Statement createAssignStatement(String variableName, exprType expression){
        return new AssignStatement(variableName,parseExpression(expression));
    }
    public Expression createFunctionCallExpression(String functionName, List<Expression> parameterValues) {
        return new FunctionCallExpression(functionName, parameterValues);
    }

    public Expression parseExpression(exprType expression){
        if(expression instanceof BinOp){
            BinOp b = (BinOp) expression;
            Expression left = parseExpression(b.left);
            Expression right = parseExpression(b.right);
            return new BinOpExpression(left,right,b.op);
        }
        if(expression instanceof Compare){
            Compare compare = (Compare) expression;
            Expression left = parseExpression(compare.left);
            Expression right = parseExpression(compare.right);
            switch (compare.ops){
                case Gt:
                    return new GTConditionExpression(left,right);
                case LtE:
                    return new GTEConditionExpression(right,left);
                case Lt:
                    return new GTConditionExpression(right,left);
                case GtE:
                    return new GTEConditionExpression(left,right);
                case Eq:
                    return new EqualExpression(left,right,true);
                case NotEq:
                    return new EqualExpression(left,right, false);
                default:
                    return new ConstantExpression(new PyBoolean(true));
            }

        }
        if(expression instanceof BoolOp){
            // TODO: 完成对BoolOp的解析
            // return new BoolOpExpression(expressions,boolOp.op);
        }
        if(expression instanceof Num){
            Num n = (Num) expression;
            return new ConstantExpression(n.n);
        }
        if(expression instanceof Str){
            Str s = (Str) expression;
            return new ConstantExpression(s.s);
        }
        if(expression instanceof Call){
            String functionName = getNameVal((Name) ((Call) expression).func);
            List<Expression> pyObjectList = new ArrayList<>();
            if(((Call) expression).args != null) {
                for (exprType arg : ((Call) expression).args) {
                    pyObjectList.add(parseExpression(arg));
                }
            }
            return createFunctionCallExpression(functionName,pyObjectList);
        }
        if(expression instanceof Name){
            Name n = (Name) expression;
            return new VariableExpression(new PyVar(n.id));
        }
        if(expression instanceof NameConstant){
            NameConstant n = (NameConstant) expression;
            return new ConstantExpression(n.value);
        }
        if(expression instanceof UnaryOp){
            UnaryOp unaryOp = (UnaryOp) expression;
            return new UnaryExpression(parseExpression(unaryOp.operand),unaryOp.op);
        }
        return new ConstantExpression(new PyLong(123));
    }

    public String getNameVal(Name expr){
        return expr.getId();
    }
}
