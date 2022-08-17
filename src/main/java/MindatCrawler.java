import java.awt.*;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.io.*;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class MindatCrawler {
    public CrawlerRobot bot;
    private ArrayList<String> keywordsList;
    private static int NUMBER_OF_KEY_EACH_TURN = 1;
    private static int SCROLL_WAIT = 3;
    private static int NUMBER_OF_END_PAGE = 100;

    private static String DOWNLOAD_FOLDER = "/home/billy/Downloads/MindatHTML";
    public MindatCrawler(String keywordfile) throws AWTException, IOException {
        bot = new CrawlerRobot();
        readKeywordList(keywordfile);
    }

    public void run() throws IOException, InterruptedException {
        int index = 0;
        int turns = keywordsList.size();
        for (int i=0;i< turns;i++){
            String keyword = keywordsList.get(i);
            crawler(keyword);
        }
    }

    private void readKeywordList(String keywordfile) throws IOException {
        keywordsList = new ArrayList<>();
        BufferedReader reader;
        reader = new BufferedReader(new FileReader(keywordfile));
        String line;
        while ((line = reader.readLine()) != null){
            line = line.trim();
            if (line.length()==0){
                continue;
            }
            keywordsList.add(line);
        }
        reader.close();
    }

    public void printKeywordList(){
        keywordsList.forEach(e -> System.out.println(e));
    }

    public File getLatestFile(){
        File directory = new File(DOWNLOAD_FOLDER);
        File[] files = directory.listFiles(File::isFile);
        File lastModifyFile = Arrays.stream(files).max(Comparator.comparingLong(f -> f.lastModified())).orElse(null);
        return lastModifyFile;
    }

    public void checkCaptcha(){
        File lastFile = getLatestFile();
        if (lastFile == null){
            return;
        }
        String content = readHTML(lastFile);

        if (content.contains("fpsearcha")){
            return;
        }else{
            System.out.println("Please remove captcha!!");

            Scanner in = new Scanner(System.in);
            return;
        }
    }

    public String readHTML(File htmlFile){
        StringBuilder contentBuilder = new StringBuilder();
        try {
            BufferedReader in = new BufferedReader(new FileReader(htmlFile));
            String str;
            while ((str = in.readLine()) != null) {
                contentBuilder.append(str);
            }
            in.close();
        } catch (IOException e) {
        }
        String content = contentBuilder.toString();
        return content;
    }


    public void crawler(String keyword) throws InterruptedException, IOException {
        //open Chrome
        bot.openChrome();
        TimeUnit.SECONDS.sleep(1);
//        bot.changeTab();
        //enter url
        bot.typeString(String.format("https://www.mindat.org/photoscroll.php?frm_id=pscroll&cform_is_valid=1&searchbox=%s&submit_pscroll=Search", keyword));
        bot.press(KeyEvent.VK_ENTER);
        TimeUnit.SECONDS.sleep(1);
        //scroll down
        for (int i=0;i<NUMBER_OF_END_PAGE;i++){
            bot.endPage();
            TimeUnit.SECONDS.sleep(SCROLL_WAIT);
        }
        //save
        bot.save(keyword);

        //check captcha
        checkCaptcha();
        //close Chrome
        bot.closeTab();
    }
}
