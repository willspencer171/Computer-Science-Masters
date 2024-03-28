import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 * Contains methods for parsing event information as specified in an event listing.
 * Individual event listings will contain an event type, one or more participant
 names,
 * and a date. The parseEvent() method is the main driver, which bundles the output
 * from parseEventType(), parseNames(), and parseDate() into a single String
 containing
 * the information extracted from the original event listing.
 *
 * Examples of input & output (ostensibly for parseEvent(), but same input is
 passed to
 * each subordinate method & output is really an aggregation of each method's
 output):
 *
 * Input: "born JOHN_A_SMITH 18851105"
 * Output: "EVENT: born; PARTICIPANTS: John A Smith; DATE: Nov 5 1885"
 *
 * Input: "married JOHN_A_SMITH & MARY_E_JONES 19090623"
 * Output: "EVENT: married; PARTICIPANTS: John A Smith, Mary E Jones; DATE: Jun 23
 1909"
 *
 */
public class Parser {
    /**
     * Parses event listing containing event type, names of participants, & date.
     * Combines output of parseEventType(), parseNames(), and parseDate() methods
     * into a single String specifying the event listing in the desired format.
     * Each portion of the event information is preceded with a descriptive tag
     * and is separated from the others with a semi-colon.
     *
     * @param input String containing event listing
     * @return String describing event with type, participants names, & date
     */
    public static String parseEvent(String input) {
        if (input == null)
            return "EVENT: unknown; PARTICIPANTS: none; DATE: unknown";
        return "EVENT: " + parseEventType(input) + "; " +
                "PARTICIPANTS: " + parseNames(input) + "; " +
                "DATE: " + parseDate(input);
    }
    /**
     * Determines event type specified in input String & returns it as output.
     * Event type must appear as a single word consisting entirely as lower-case
     * letters appearing at the beginning of the input String, otherwise a
     * truncated event type or 'unknown' may be returned.
     *
     * @param input String in which to search for event type
     * @return String specifying event type, or 'unknown'
     */
    public static String parseEventType(String input) {
        if (input == null)
            return "unknown";
// needle: one or more contiguous lower-case characters at beginning of String
// followed by space
        Pattern pattern = Pattern.compile("^[a-z]+ ");
// haystack: String in which to look for event type
        Matcher matcher = pattern.matcher(input);
        if (matcher.find()) { // does the haystack contain an instance of the needle?
            return matcher.group().trim(); // trim off whitespace & return
        } else { // no match? input apparently doesn't contain a date
            return "unknown";
        }
    }
    /**
     * Looks for names of participants in event listing & returns them listed in
     a String.
     * Names must be in all caps, with underscores (rather than spaces)
     separating first,
     * last, and middle names. Individual names should be separated from each
     other with
     * spaces and ampersands, as in 'A_B & X_Y.' Output String will contain list
     of names
     * separated by commas, with each name reformatted from (for example)
     'JOHN_A_SMITH'
     * into "John A Smith." If no participant names are found, 'none' is
     returned.
     *
     * @param input String in which to search for participant names
     * @return String containing list of participant names, or 'none'
     */
    protected static String parseNames(String input) {
        if (input == null)
            return "none";
// needle: one or more contiguous upper-case characters, possibly interspersed
// with underscores, and with leading & trailing spaces
        Pattern pattern = Pattern.compile(" [A-Z|\\_]+ ");
// haystack: String in which to look for names
        Matcher matcher = pattern.matcher(input);
        StringBuilder names = new StringBuilder("none");
// continue as we find more & more instances of needle in haystack
        while (matcher.find()) {
/* trim whitespace, convert to lower-case, replace underscores
with spaces,
* and capitalize the first letter of each first/middle/last name
*/
            String thisName = matcher.group().trim().toLowerCase();
            thisName = thisName.replace("_", " ");
            thisName = capitalizeFirst(thisName);
            if (names.toString().equals("none")) { // first name found
                names = new StringBuilder(thisName);
            } else { // subsequent names
                names.append(", ").append(thisName); // separate names with commas
            }
        }
        return names.toString();
    }
    /**
     * Finds date specified in event listing, reformats it, & returns it as a
     String.
     * Date must be in 'yyyyMMdd' format (e.g. 20090908 for September 8, 2009),
     and must
     * be separated from other elements in event listing by a space. Output
     String will
     * contain date reformatted into 'MMM d yyyy' format (e.g. Sep 8 2009). If no
     date
     * is found, 'unknown' is returned.
     *
     * @param input String in which to search for date
     * @return String containing date in human-readable output format
     */
    protected static String parseDate(String input) {
        if (input == null)
            return "unknown";
// needle: one or more contiguous numeric digits, preceded by a space
        Pattern pattern = Pattern.compile(" \\d+");
// haystack: String in which to look for Date
        Matcher matcher = pattern.matcher(input);
        if (matcher.find()) { // does the haystack contain an instance of the needle?
                    DateFormat dfIn = new SimpleDateFormat("yyyyMMdd"); // input date format
            DateFormat dfOut = new SimpleDateFormat("MMM d yyyy"); // output date format
            try {
/* trim whitespace, then parse the match using the input
format,
* convert into the output format, and return
*/
                return dfOut.format(dfIn.parse(matcher.group().trim()));
            } catch (ParseException e) {
// error: mal-formed date field, ignore for now
                return "unknown";
            }
        } else { // no match? this input apparently doesn't contain a date
            return "unknown";
        }
    }
    /**
     * Capitalizes first letter of each individual word of a larger String.
     *
     * @param input String to be capitalized
     * @return original String with first letter of each individual word
    capitalized
     */
    protected static String capitalizeFirst(String input) {
        if (input == null)
            return "";
        String[] words = input.split("\\s+"); // split input String by spaces into Array
        StringBuilder output = new StringBuilder();
        for (String word : words) // for each individual word in words array
        // capitalize first letter in each word & reassemble into output String
            output.append(word.substring(0, 1).toUpperCase()).append(word.substring(1)).append(" ");
        return output.toString().trim();
    }
}
