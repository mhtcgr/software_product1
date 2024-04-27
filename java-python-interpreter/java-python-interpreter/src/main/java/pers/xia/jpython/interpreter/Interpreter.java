package pers.xia.jpython.interpreter;

import pers.xia.jpython.ast.Module;
import pers.xia.jpython.ast.*;
import pers.xia.jpython.grammar.GramInit;
import pers.xia.jpython.interpreter.expression.ConstantExpression;
import pers.xia.jpython.interpreter.expression.Expression;
import pers.xia.jpython.interpreter.statement.*;
import pers.xia.jpython.object.PyExceptions;
import pers.xia.jpython.object.PyLong;
import pers.xia.jpython.parser.Ast;
import pers.xia.jpython.parser.Node;
import pers.xia.jpython.parser.ParseToken;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class Interpreter {
    private final List<Statement> statements = new ArrayList<>();
    public static ProgramState programState = new ProgramState();
    /** initialize the print function */
    static {
        List<String> parNames = new ArrayList<>();
        parNames.add("arg");
        List<Statement> statementList = new ArrayList<>();
        statementList.add(new PrintStatement());
        programState.registerFunction("print",parNames,statementList);
    }
    public Interpreter() {
    }
    public Interpreter(List<stmtType> nodes){
        for (stmtType node : nodes) {
            Statement statement = parseAstNode(node);
            statements.add(statement);
        }
    }
    /** running the program */
    public void runProgram() {
        for (Statement statement: statements) {
            statement.run(programState);
        }
    }

    private Statement parseAstNode(stmtType node){
        Parser parser = new Parser();
        if(node instanceof Assign){
            // Todo: 实现连续赋值 比如a=b=1
            String variableName;
            exprType target = ((Assign) node).targets.get(0);
            variableName = parser.getNameVal((Name) target);
            exprType value = ((Assign) node).value;
            Expression expression = parser.parseExpression(value);
            return new AssignStatement(variableName,expression);
        }
        if (node instanceof For){
            For forNode = (For) node;
            if(!(forNode.target instanceof Name) || !(forNode.iter instanceof Call)){
                return new EmpytStatement();
            }
            String variableName = ((Name) forNode.target).getId();
            Call range = (Call) forNode.iter;
            if(!(range.func instanceof Name)  || !((Name) range.func).getId().equals("range")){
                return new EmpytStatement();
            }
            Expression start = range.args.size() > 1 ? parser.parseExpression(range.args.get(0)) : new ConstantExpression(new PyLong(0));
            Expression end = range.args.size() > 1 ? parser.parseExpression(range.args.get(1)) : parser.parseExpression(range.args.get(0));
            //Todo：从range中提取第3个参数
            List<Statement> body = new ArrayList<>();
            List<Statement> elseBody = new ArrayList<>();
            for(stmtType statement: forNode.body ){
                body.add(parseAstNode(statement));
            }
            if(forNode.orelse != null) {
                for(stmtType stmt: forNode.orelse){
                    elseBody.add(this.parseAstNode(stmt));
                }
            }
            return new ForStatement(variableName,start,end,body);
        }
        if (node instanceof If){
            If ifNode = (If) node;
            Expression test = parser.parseExpression(ifNode.test);
            List<Statement> body = new ArrayList<>();
            List<Statement> elseBody = new ArrayList<>();
            for(stmtType stmt: ifNode.body){
                body.add(this.parseAstNode(stmt));
            }
            if(ifNode.orelse != null) {
                for(stmtType stmt: ifNode.orelse){
                    elseBody.add(this.parseAstNode(stmt));
                }
            }
            return new IfStatement(test,body,elseBody);
        }
        if(node instanceof While){
            While whileNode = (While) node;
            //Todo 实现对While的解析
            // return new WhileStatement(test,body,elseBody);
        }
        if (node instanceof Expr){
            exprType target = ((Expr) node).value;
            Expression expression = parser.parseExpression(target);
            return new ExprStatement(expression);
        }
        if(node instanceof FunctionDef){
            FunctionDef funNode = (FunctionDef) node;
            List<String> parameterNames = new ArrayList<>();
            if(funNode.args.args!=null){
                for(argType arg: funNode.args.args){
                    parameterNames.add(arg.arg);
                }
            }
            List<Statement> statements= new ArrayList<>();
            for(stmtType stmt:funNode.body){
                statements.add(parseAstNode(stmt));
            }
            return new DefineFunctionStatement(funNode.name,parameterNames,statements);
        }
        if (node instanceof Return){
            Return returnNode = (Return) node;
            Expression expression = parser.parseExpression(returnNode.value);
            return new ReturnStatement(expression);
        }
        if (node instanceof Continue){
            return new ContinueStatement();
        }
        if (node instanceof Break){
            return new BreakStatement();
        }
        return  new EmpytStatement();
    }

    public static void main(String[] args) {
        String fileName = "src/test/resources/InterpreterTask2.py";
        File file = new File(fileName);
        try
        {
            Node node = ParseToken.parseFile(file, GramInit.grammar, 1);
            Ast ast = new Ast();
            Module mod = (Module) ast.fromNode(node);
            Interpreter interpreter = new Interpreter(mod.getBody());
            interpreter.runProgram();
        }
        catch (PyExceptions e)
        {
            System.out.println(fileName);
            e.printStackTrace();
            throw e;
        }
    }
}
