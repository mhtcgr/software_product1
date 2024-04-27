package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.ast.unaryopType;
import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.PyBoolean;
import pers.xia.jpython.object.PyObject;

public class UnaryExpression extends Expression{
    Expression operand;
    unaryopType type;
    public UnaryExpression(Expression operand,unaryopType type){
        this.operand = operand;
        this.type = type;
    }

    @Override
    public PyObject eval(ProgramState programState) {
        PyObject res = operand.eval(programState);
        switch (type){
            case UAdd:
                return res;
            case Not:
                return new PyBoolean(!res.asBoolean());
            case USub:
                return res.uSub();
            default:
                return res; // 未实现
        }

    }
}
