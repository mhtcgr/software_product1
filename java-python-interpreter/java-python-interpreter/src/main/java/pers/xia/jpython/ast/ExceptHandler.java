// Autogenerated AST node
package pers.xia.jpython.ast;
import pers.xia.jpython.object.PyObject;
import java.io.DataOutputStream;
import java.io.IOException;

public class ExceptHandler extends excepthandlerType {
    public exprType type;
    public String name;
    public java.util.List<stmtType> body;

    public ExceptHandler(exprType type, String name,
    java.util.List<stmtType> body,int lineno, int col_offset) {
        this.type = type;
        this.name = name;
        this.body = body;
        this.lineno = lineno;
        this.col_offset = col_offset;
    }

    public String toString() {
        return "ExceptHandler";
    }

    public void pickle(DataOutputStream ostream) throws IOException {
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitExceptHandler(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
    }

}
