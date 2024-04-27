package pers.xia.jpython.interpreter.expression;

import pers.xia.jpython.interpreter.ProgramState;
import pers.xia.jpython.object.*;

public class GTEConditionExpression extends OpExpression{

    public GTEConditionExpression(Expression lhs, Expression rhs){
        super(lhs, rhs);
    }

    @Override
    public PyObject eval(ProgramState programState) {
        PyObject lhs = this.lhs.eval(programState);
        PyObject rhs = this.rhs.eval(programState);
        boolean res = false;
        if(lhs instanceof PyUnicode && rhs instanceof PyUnicode){
            res = ((PyUnicode) lhs).compare((PyUnicode) rhs) >= 0;
        }else{
            PyObject p= lhs.sub(rhs);
            if(p instanceof PyLong){
                res = ((PyLong) p).asLong() >= 0;
            }
            else if(p instanceof PyFloat){
                res = ((PyFloat) p).asFloat() >= 0;
            }
        }
        return new PyBoolean(res);
    }
}
