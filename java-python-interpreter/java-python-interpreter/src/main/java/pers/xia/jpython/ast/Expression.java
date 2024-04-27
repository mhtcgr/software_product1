// Autogenerated AST node
package pers.xia.jpython.ast;
import pers.xia.jpython.object.PyObject;
import java.io.DataOutputStream;
import java.io.IOException;

public class Expression extends modType {
    public exprType body;

    public Expression(exprType body) {
        this.body = body;
    }

    public String toString() {
        return "Expression";
    }

    public void pickle(DataOutputStream ostream) throws IOException {
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitExpression(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
    }

}
