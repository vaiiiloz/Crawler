import java.awt.*;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.io.IOException;
import java.util.Locale;
import java.util.concurrent.TimeUnit;

public class CrawlerRobot {
    private Robot robot;
    private String OS;

    public CrawlerRobot() throws AWTException {
        robot = new Robot();
        OS = System.getProperty("os.name").toLowerCase();
    }

    public void click(int x, int y, int mask) throws InterruptedException {
        robot.mouseMove(x,y);
        TimeUnit.SECONDS.sleep(1);
        robot.mousePress(mask);
        robot.mouseRelease(mask);
    }

    public void testClick(int x, int y) throws InterruptedException {
        click(x, y, InputEvent.BUTTON3_MASK);
    }

    public void press(int mask){
        robot.keyPress(mask);
        robot.keyRelease(mask);
    }

    public void typeString(String keyword){
        StringSelection stringSelection = new StringSelection(keyword);
        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
        clipboard.setContents(stringSelection, stringSelection);

        robot.keyPress(KeyEvent.VK_CONTROL);
        robot.keyPress(KeyEvent.VK_V);
        robot.keyRelease(KeyEvent.VK_V);
        robot.keyRelease(KeyEvent.VK_CONTROL);
    }

    public void changeTab(){
        robot.keyPress(KeyEvent.VK_ALT);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_ALT);
    }

    public void closeTab(){
        robot.keyPress(KeyEvent.VK_ALT);
        robot.keyPress(KeyEvent.VK_F4);
        robot.keyRelease(KeyEvent.VK_F4);
        robot.keyRelease(KeyEvent.VK_ALT);
    }

    public void save(String filename) throws InterruptedException {



        robot.keyPress(KeyEvent.VK_CONTROL);
        robot.keyPress(KeyEvent.VK_S);
        robot.keyRelease(KeyEvent.VK_S);
        robot.keyRelease(KeyEvent.VK_CONTROL);
        TimeUnit.SECONDS.sleep(1);

        if (OS.contains("nux")){
            changeTab();
            TimeUnit.SECONDS.sleep(1);

            changeTab();
            TimeUnit.SECONDS.sleep(1);
        }

        typeString(filename);

        enter();

        enter();
    }

    public void enter() throws InterruptedException {
        robot.keyPress(KeyEvent.VK_ENTER);
        robot.keyRelease(KeyEvent.VK_ENTER);
        TimeUnit.SECONDS.sleep(1);

    }

    public void endPage(){
        robot.keyPress(KeyEvent.VK_END);
        robot.keyRelease(KeyEvent.VK_END);
    }

    public void openChrome() throws IOException, InterruptedException {

        if (OS.contains("win")){
            Process p = Runtime.getRuntime().exec(new String[]{"cmd", "/c", "start chrome"});
            p.waitFor();
        }
        if (OS.contains("nux")){
            Process p = Runtime.getRuntime().exec(new String[]{"bash", "-c", "/opt/google/chrome/chrome"});


            p.waitFor();
        }

        robot.keyPress(KeyEvent.VK_F11);
        robot.keyRelease(KeyEvent.VK_F11);
    }
}
