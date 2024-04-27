
import org.junit.jupiter.api.AfterEach;

import org.junit.jupiter.api.Test;
import pers.xia.jpython.main.REPL;
import pers.xia.jpython.object.PyExceptions;

import utils.AuthorAndTime;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.Assert.assertEquals;

@AuthorAndTime(author = "wangzhen",time = "2023/06/18")
public class PyReadModTest {
    public static ByteArrayOutputStream outContent=null;
    private final PrintStream originalOut = System.out;
    static {
        // 捕获 stdout 并运行代码
        outContent= new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
    }
    @AfterEach
    public void cleanUp() {
        // 恢复原始的 System.out 输出流
        System.setOut(originalOut);
        // 清空 outContent 的缓存内容
        outContent.reset();
    }
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    private static void testCode(String input,String expectedOutput ){
        try
        {
            REPL.PyReadMod mod = new REPL.PyReadMod(input);
            int num = mod.getIndentationLevel();
            String result = mod.format();
            System.out.println("(" + num + " " + result + ")");
            String printedOutput = outContent.toString().trim();
            System.out.println(printedOutput);
            // 检查输出是否正确
            assertEquals(expectedOutput, printedOutput);
        }
        catch (PyExceptions e)
        {
            System.out.println(input);
            e.printStackTrace();
            throw e;
        }
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void task1(){
        String input="print(12) #123";
        String expectedOutput="(0 print(12))";
        testCode(input,expectedOutput);
    }

    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void task2(){
        String input="    print(123)";
        String expectedOutput="(4 print(123))";
        testCode(input,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void task3(){
        String input="print(\"123\")";
        String expectedOutput="(0 print(\"123\"))";
        testCode(input,expectedOutput);
    }
    @Test
    @AuthorAndTime(author = "wangzhen",time = "2023/06/18")
    public void task3_1(){
        String input="print('ab\"c\"')";
        String expectedOutput="(0 print('ab\"c\"'))";
        testCode(input,expectedOutput);
    }
}
