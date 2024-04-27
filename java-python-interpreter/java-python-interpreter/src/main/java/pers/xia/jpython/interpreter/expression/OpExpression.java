package pers.xia.jpython.interpreter.expression;

public abstract class OpExpression extends Expression{
    protected Expression lhs;
    protected Expression rhs;

    public OpExpression(Expression lhs, Expression rhs) {
        this.lhs = lhs;
        this.rhs = rhs;
    }
}
