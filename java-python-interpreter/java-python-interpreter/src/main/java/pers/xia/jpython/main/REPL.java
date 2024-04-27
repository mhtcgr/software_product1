package pers.xia.jpython.main;

import pers.xia.jpython.ast.Module;
import pers.xia.jpython.grammar.GramInit;
import pers.xia.jpython.interpreter.Interpreter;
import pers.xia.jpython.interpreter.statement.Statement;
import pers.xia.jpython.object.Py;
import pers.xia.jpython.object.PyExceptions;
import pers.xia.jpython.parser.Ast;
import pers.xia.jpython.parser.Node;
import pers.xia.jpython.parser.ParseToken;
import pers.xia.jpython.parser.Parser;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.Stack;

public class REPL {
    private static boolean pyReadMode =false;

    public static void main(String[] args) {
        driverLoop();
    }

    private static void driverLoop() {
        while (true) {
            System.out.print(">>> ");
            String input = readInput();
            if (input == null) {
                break;
            }
            if (input.equals("exit")) {
                break;
            }
            if (input.equals("PYREAD")){
                pyReadMode = true;
                pyReadLoop();
                continue;
            }
            try {
                evalLine(input);
            } catch (Exception e) {
                // Handle exceptions here
                e.printStackTrace();
            }
        }
    }

    private static String readInput() {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            return reader.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private static void evalLine(String line) {
        // Implement your evaluation logic here
        // Replace this with the actual evaluation code
        PyReadMod mod = new PyReadMod(line);
        StringBuilder st = new StringBuilder();

        while (!mod.isEnd()){
            st.append(mod.format()).append("\n");
            System.out.print("...");
            line = readInput();
            mod = new PyReadMod(line);
        }
        String formatStr = mod.format();
        st.append(formatStr).append("\n");
        byte[] bytes = st.toString().getBytes();

        Node node = ParseToken.parseBytes(bytes, GramInit.grammar, 1);
        Ast ast = new Ast();
        // get the modType
        Module module = (Module) ast.fromNode(node);
        Interpreter interpreter = new Interpreter(module.getBody());
        interpreter.runProgram();
    }
    private static void pyReadLoop() {
        while (true) {
            System.out.print(">>>(Py-read) ");
            String input = readInput();
            if (input == null) {
                break;
            }
            if (input.equals("exit")) {
                pyReadMode = false;
                break;
            }
            try {
                PyReadMod mod = new PyReadMod(input);
                int num = mod.getIndentationLevel();
                String result = mod.format();
                System.out.println("(" + num + " " + result + ")");
            } catch (Exception e) {
                // Handle exceptions here
                e.printStackTrace();
            }
        }
    }
    public static class PyReadMod {
        static Map<Character,Character> mp = new HashMap<>();
        static {
            mp.put('{','}');mp.put('(',')');mp.put('[',']');
            mp.put(':','\0');
        }
        private String line;
        static Stack<Character> st = new Stack<>();
        public PyReadMod(String line) {
            this.line = line;
        }
        public String format(){
            StringBuilder sb = new StringBuilder();
            while (line.length()>0){
                Character c = peekChar();
                if(isNumber(c)&&sb.length()==0){ // number case
                    String appendStr = getFormatNum(line);
                    sb.append(appendStr);
                    break;
                }else if(isComment(c)){         //comment case
                    String appendStr = ignoreComment();
                    sb.append(appendStr);
                    while(sb.charAt(sb.length()-1) == ' '){
                        sb.delete(sb.length()-2, sb.length()-1);
                    }
                }
                else if(isString(c)){          //string case
                    String appendStr = getFormatString(c);
                    sb.append(appendStr);
                }else {
                    sb.append(readChar());
                }
            }
            return sb.toString();
        }

        private Character peekChar(){
            if(line.length()>0) return line.charAt(0);
            return null;
        }
        private Character readChar(){
            if(line.length()>0){
                char c = line.charAt(0);
                line = line.substring(1);
                return c;
            }
            return null;
        }
        private String ignoreComment(){
            // function to be implemented
            while (peekChar()!=null){
                //sb.append(readChar());
                readChar();}
            String a = " ";
            return a;
        }
        public int getIndentationLevel(){
            formatEscape();
            // function to be implemented;
            char a = peekChar();
            int res = 0;
            while(a == 0){
                readChar();
                res++;
                a = peekChar();
            }
            return res;
        }

        private String getFormatString(Character ch){
            StringBuilder sb = new StringBuilder();
            sb.append(readChar());
            if(ch == '\''){
                while(peekChar() != '\''){
                    sb.append(readChar());
                }
                sb.append(readChar());
            } else if (ch == '\"') {
                while (peekChar() != '\"'){
                    sb.append(readChar());
                }
                sb.append(readChar());
            }
            return sb.toString();
            /* sb is a StringBuilder Class, you can use append() to add a char and toString() to
                convert it to a string class.
            */
            // function to be implemented, and delete the exception clause;
        }

        private String getFormatDouble(String line){
            // function to be implemented;
            return new String("");
        }
        private String getFormatNum(String line){
            return "print(" + line + ")";
        }

        private boolean isNumber(Character c){
            return c>='0'&& c<='9';
        }
        private boolean isComment(Character c){
            return c == '#';
        }
        private boolean isString(Character c){
            return c.equals('\"')||c.equals('\'');
        }
        private boolean isDouble(Character c){ return c.equals('.');}
        private boolean isEnd(){
            char[] chars = line.toCharArray();
            while (chars.length==0&&!st.isEmpty()){
                if(st.peek()==':')st.pop();
                else break;
            }
            for (char aChar : chars) {
                if(mp.containsKey(aChar)){
                    st.push(aChar);
                }else {
                    if(st.isEmpty()) continue;
                    if(mp.get(st.peek()) != aChar) continue;
                    st.pop();
                }
            }
            return st.isEmpty();
        }
        private void formatEscape() {
            line = line.replace("\t","    ");
        }
        public int getNumBeforeDot(String s){
            char[] chars = s.toCharArray();
            int res = 0;
            for (int i = chars.length-1; i >= 0 ; i--) {
                if(isNumber(chars[i])){
                    res += res*10 + (chars[i]-'0');
                }else {
                    break;
                }
            }
            return res;
        }
    }
}
