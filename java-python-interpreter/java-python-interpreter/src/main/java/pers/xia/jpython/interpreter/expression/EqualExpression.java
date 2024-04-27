package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.*;

public class EqualExpression extends OpExpression{

    boolean equal;

    public EqualExpression(Expression lhs, Expression rhs, boolean equal) {
        super(lhs, rhs);
        this.equal = equal;
    }

    @Override
    public PyObject eval(ProgramState programState) {
        PyObject lhs = this.lhs.eval(programState);
        PyObject rhs = this.rhs.eval(programState);
        boolean res;
        if(lhs instanceof PyUnicode && rhs instanceof PyUnicode){
            res = ((PyUnicode) lhs).compare((PyUnicode) rhs) != 0;
        }else{
            res = lhs.equals(rhs);
        }
        return new PyBoolean(equal ? res : !res);
    }
}
