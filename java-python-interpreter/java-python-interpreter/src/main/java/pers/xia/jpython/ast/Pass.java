// Autogenerated AST node
package pers.xia.jpython.ast;
import pers.xia.jpython.object.PyObject;
import java.io.DataOutputStream;
import java.io.IOException;

public class Pass extends stmtType {

    public Pass(int lineno, int col_offset) {
        this.lineno = lineno;
        this.col_offset = col_offset;
    }

    public String toString() {
        return "Pass";
    }

    public void pickle(DataOutputStream ostream) throws IOException {
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitPass(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
    }

}