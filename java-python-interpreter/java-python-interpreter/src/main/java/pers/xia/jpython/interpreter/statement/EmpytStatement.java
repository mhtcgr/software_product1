package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;

public class EmpytStatement implements Statement {
    @Override
    public void run(ProgramState programState) {
        throw new RuntimeException("unknow Statement error exception");
    }
}
