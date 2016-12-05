package linkcrawler;

import java.io.*;
import java.net.*;
import java.util.regex.*;

public class JavaSpider {
	public  String UrlCrawler(String url) {
		// 定义一个字符串用来存储网页内容
		String result = "";
		// 定义一个缓冲字符输入流
		BufferedReader in = null;

		try {
			// 将string转成url对象
			URL realUrl = new URL(url);
			// 初始化一个链接到那个url的连接
			URLConnection connection = realUrl.openConnection();
			// 开始实际的连接
			connection.connect();
			// 初始化 BufferedReader输入流来读取URL的响应
			in = new BufferedReader(new InputStreamReader(
					connection.getInputStream(),"utf-8"));//指定编码方式
			// 用来临时存储抓取到的每一行的数据
			String line;
			while ((line = in.readLine()) != null) {
				// 遍历抓取到的每一行并将其存储到result里面
				result += line;
			}
		} catch (Exception e) {
			System.out.println("发送GET请求出现异常！" + e);
			e.printStackTrace();
                        return "error";
		}
		// 使用finally来关闭输入流
		finally {
			try {
				if (in != null) {
					in.close();
				}
			} catch (Exception e2) {
				e2.printStackTrace();
			}
		}
		return result;

	}

	public Matcher regexString(String targetStr, String patternStr) {
		// 定义一个样式模板，此中使用正则表达式，括号中是要抓的内容
		// 相当于埋好了陷阱匹配的地方就会掉下去
		Pattern pattern = Pattern.compile(patternStr, Pattern.DOTALL);
		// 定义一个matcher用来做匹配
		Matcher matcher = pattern.matcher(targetStr);
                return matcher;
	}

	public static void main(String[] args) {

		// 定义即将访问的链接
		String url = "http://news.sina.com.cn/s/wh/2016-11-30/doc-ifxyawxa3150010.shtml?cre=newspagepc&mod=f&loc=5&r=9&doct=0&rfunc=16";  
                JavaSpider js = new JavaSpider();
		String result = js.UrlCrawler(url);
		Matcher urlMatcher = js.regexString(result, "href=\"(http[s]?.*?)\"");
                Matcher titleMatcher = js.regexString(result, "<h1 id=\"artibodyTitle\".*?>(.*?)</h1>");
                Matcher timeMatcher = js.regexString(result, "<span.*?id=\"navtimeSource\">(.*?)<span>");
                Matcher contentMatcher = js.regexString(result, "<div.*?id=\"artibody\">(.*?)</div>");
                String allContent = null;
                if(contentMatcher.find()){
                    allContent = contentMatcher.group(1);
                }
                Matcher contentLineMatcher = js.regexString(allContent, "<p.*?>(.*?)</p>");
//                while (urlMatcher.find()){
//                    System.out.println(urlMatcher.group(1));
//                }
                while (titleMatcher.find()){
                    System.out.println(titleMatcher.group(1));
                }
                while (timeMatcher.find()){
                    System.out.println(timeMatcher.group(1));
                }
		while (contentLineMatcher.find()){
                    System.out.println(contentLineMatcher.group(1).replaceAll("<.*?>", "").replaceAll("&nbsp", ""));
                }
	}
}