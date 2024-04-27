package pers.xia.jpython.interpreter.statement;

import pers.xia.jpython.interpreter.ProgramState;

public interface Statement {
    void run(ProgramState programState);
}
