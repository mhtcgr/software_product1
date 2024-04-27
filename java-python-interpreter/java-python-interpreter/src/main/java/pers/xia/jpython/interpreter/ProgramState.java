package pers.xia.jpython.interpreter;

import pers.xia.jpython.interpreter.statement.Statement;
import pers.xia.jpython.object.PyExceptions;
import pers.xia.jpython.object.PyObject;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;

public class ProgramState {
    protected final HashMap<String, PyObject> variableHeap;
    protected final Stack<FunctionState> functionStateStack;
    protected final Map<String, List<String>> stringList;
    protected final Map<String, List<Statement>> statementList;
    protected final PyExceptions pyExceptions;

    public ProgramState() {
        variableHeap = new HashMap<>();
        functionStateStack = new Stack<>();
        stringList = new HashMap<>();
        statementList = new HashMap<>();
        pyExceptions = new PyExceptions();
    }
        /** Returns the integer value associated with the specified variable name in the current call frame. */
        public PyObject getVariable(String variable) {
            HashMap<String, PyObject> topCallFrame = variableHeap;
            if (!topCallFrame.containsKey(variable)) {
                if(!functionStateStack.isEmpty()){
                    FunctionState peek = functionStateStack.peek();
                    if(!peek.hasVariable(variable)){
                        throw new RuntimeException("Undefined variable: " + variable);
                    }else {
                        return peek.getVariable(variable);
                    }
                }else {
                    throw new RuntimeException("Undefined variable: " + variable);
                }
            }else {
                if(!functionStateStack.isEmpty()&& functionStateStack.peek().hasVariable(variable)){
                    FunctionState peek = functionStateStack.peek();
                    return peek.getVariable(variable);
                }
            }
            return topCallFrame.get(variable);
        }
    /** Returns the boolean value whether the specified variable name exists in the global frame. */
    public boolean hasVariable(String variable) {
        return variableHeap.containsKey(variable);
    }
    public void setVariable(String variableName,PyObject object){
        variableHeap.put(variableName,object);
    }

    public void updateException(String err){
        pyExceptions.addException(err);
    }
    public FunctionState getTopFunctionState(){
        if(!functionStateStack.isEmpty()){
            return functionStateStack.peek();
        }
        return null;
    }

    public Stack<FunctionState> getFunctionStateStack() {
        return functionStateStack;
    }

    /** Returns the list of parameter names associated with the specified function name. */
    public void registerFunction(String functionName, List<String> parameterNames, List<Statement> functionStatements) {
        stringList.put(functionName, parameterNames);
        statementList.put(functionName, functionStatements);
    }

    /** Returns the list of parameter names associated with the specified function name. */
    public List<String> getParameterNames(String functionName) {
        if (stringList.isEmpty() == true) {
            System.out.println("Sorry there are no parameters");
        }
        return stringList.get(functionName);

    }

    /** Returns the list of function statements associated with the specified function name. */
    public List<Statement> getFunctionStatements(String functionName) {
        if(statementList.isEmpty() == true){
            System.out.println("Sorry there are no statements in the function");
        }
        return statementList.get(functionName);
    }
}
