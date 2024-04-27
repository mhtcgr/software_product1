package pers.xia.jpython.main;

import java.io.File;

import pers.xia.jpython.ast.Module;
import pers.xia.jpython.ast.modType;
import pers.xia.jpython.ast.stmtType;
import pers.xia.jpython.grammar.GramInit;
import pers.xia.jpython.object.PyExceptions;
import pers.xia.jpython.parser.Ast;
import pers.xia.jpython.parser.Node;
import pers.xia.jpython.parser.ParseToken;
import pers.xia.jpython.parser.Parser;
import pers.xia.jpython.parser.Parser.ReturnCode;
import pers.xia.jpython.tokenizer.TokState;
import pers.xia.jpython.tokenizer.Token;
import pers.xia.jpython.tokenizer.Tokenizer;

public class Run
{

    public static void parse(String fileName)
    {
        File file = new File(fileName);
        if(file.isDirectory())
            return;
        try
        {
            Node node = ParseToken.parseFile(file, GramInit.grammar, 1);
            Ast ast = new Ast();
            // get the modType
            Module mod = (Module) ast.fromNode(node);
            for (stmtType stmtType : mod.body) {
                System.out.println(stmtType.toString());
            }
        }
        catch (PyExceptions e)
        {
            System.out.println(fileName);
            e.printStackTrace();
            throw e;
        }
    }

    public static void main(String[] args)
    {
        File file = new File("./source");
        if(file.isDirectory())
        {
            String[] fileList = file.list();
            for (String fileName : fileList)
            {
                if(fileName.charAt(fileName.length() - 1) == 'y')
                    parse("./source/" + fileName);
            }
        }
    }
}
