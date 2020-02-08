# “This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)”

require 'date'


def parse_and_add_to_array(string, array)

    """ 
    Sample Whatsapp String --- 5/11/19, 11:45 PM - Adarsh: I came across a few of these on Reddit. Just a few.

    This function takes a string and parses it using the regex (when was it sent, who sent it, and what was sent.) and adds it to an array containing all messages
    
    The sent_on_date is modified to be clearer for the DateTime parser to correctly parse it. 

    If the message does not match with the pattern, it means it is part of a multi-line message and the previous entry is accordingly modified.
    """

    @pattern = /(?<day>\d{1,2})\/(?<month>\d{1,2})\/(?<year>\d{1,2}), (?<hour>\d{1,2}):(?<minute>\d{1,2}) (?<zone>AM|PM) - (?<name>[^:]+):(?<message>.+)/

    if matched_string = string.match(@pattern)
        sent_on_date = "#{matched_string[:month]}/#{matched_string[:day]}/20#{matched_string[:year]}, #{matched_string[:hour]}:#{matched_string[:minute]} #{matched_string[:zone]}"
        sent_by_name = matched_string[:name]
        sent_message = matched_string[:message]

        array.push({name:sent_by_name, time:sent_on_date, content: sent_message})
        true
    else
        array[-1][:content] = array[-1][:content] + string
        false
    end

end

def was_there_a_gap(array, gap_object)

    """ 
    Given an array of messages, determines if there was a gap of an entire day between the last sent message and the one before that and updates the relevant key in the statistics object accordingly.

    Example: Message 1 sent on 24-March-2019. Message 2 sent on 26-March-2019. Has a gap of one day, 25-March-2019.
    """
    
    if difference = (Date.parse(array[-1][:time]) - Date.parse(array[-2][:time])).to_i - 1

    end
    if difference > 0
        if gap_object[difference]
            gap_object[difference] += 1
            # debugger_print([array[-2][:time],array[-1][:time]])
        else
            gap_object[difference] = 1
        end
    else
    end
end

def estimate_minutes(array, stat_obj)
    
    """ 
    Given an array of messages, determines if the messages were sent within the same minute or on different minutes. If the messages were sent on different minutes then the statistics object is updated accordingly to reflect that. 

    Why? Assuming each message (no matter how short) takes at least 1 minute of time to formulate and send, this number would give us the lower bound of time spent.
    
    Example: Message 1 sent on 11:29 PM. Message 2 sent on 11:30PM. They are different minutes, so the minutes count gets incremented by 1.
    """
    
    difference = (DateTime.parse(array[-1][:time]) - DateTime.parse(array[-2][:time]))

    if difference > 0 
        stat_obj[:minutes_count] += 1
    else
        stat_obj[:minutes_count]
    end

end

def set_name(array, list)

    """ 
    Given an array of messages and an array of two particpants in the conversation, it determines if the names of those two participants are set or not.

    List is initially of the form [ {name:"", message_count:0, word_count:0}, {name:"", message_count:0, word_count:0} ]
    """

    if array[-1][:name] == list[0][:name] || array[-1][:name] == list[1][:name]
    elsif list[0][:name] == "" && list[1][:name] == ""
        list[0][:name] = array[-1][:name]
    else 
        list[1][:name] = array[-1][:name]
    end

end

def word_counter(array, list)

    """ 
    Given an array of messages and an array of two particpants in the conversation, it goes through the last message, counts the number of words in it and accordingly increments the word_count value for the correct particpant.
    """

    if array[-1][:name] == list[0][:name]
        list[0][:message_count] += 1
        list[0][:word_count] += array[-1][:content].split.count
    elsif array[-1][:name] == list[1][:name]
        list[1][:message_count] += 1
        list[1][:word_count] += array[-1][:content].split.count
    else
    end

end

def unique_count(array, stat_obj)

    """ 
    Given an array of messages, it determines whether the last two messages were sent on unique days or not. If yes, it increments the value of the unique_days count in the statistics object.

    Example: Message 1 sent on 24-March-2019. Message 2 sent on 25-March-2019. Since the dates are different, the count is incremented by one.
    """
    
    if not Date.parse(array[-1][:time]) == Date.parse(array[-2][:time])
        stat_obj[:unique_days] += 1
    end
    
end

def debugger_print(array_of_values)
    """ 
    Prints out the given array in an attempt to make debugging easier
    """

    puts array_of_values
    puts "~~"
end


""" 
All the variables used in this program are initialized below.
"""

messages_array = []

person_list = [ {name:"", message_count:0, word_count:0}, {name:"", message_count:0, word_count:0} ]

statistics = {minutes_count:0, unique_days: 1}

messages_gap = {}



""" 
Opens the file with the name in the argument one line at a time and runs the appropriate methods on each line.

First the line(string) is parsed and the results added to an array. The array is then analyzed to identify 
1. Name of the participants is set 
2. Word count in the message

Once more than two messages are added, we run further methods to 
3. Determine if there was a gap of more than 1 full day between the messages
4. Determine a lower bound of minutes spent on this conversation
5. Determine the total number of unique days this conversation took place in
"""

File.foreach("samplelog.txt") {
    
    |line| 

    if parse_and_add_to_array(line, messages_array)
        set_name(messages_array, person_list)
        word_counter(messages_array, person_list)

        if messages_array.size >= 2
            was_there_a_gap(messages_array, messages_gap)
            estimate_minutes(messages_array, statistics)
            unique_count(messages_array, statistics)
        end
    else
        messages_array[-1][:content] = messages_array[-1][:content] + line
        # word_counter(messages_array, person_list)
    end

}


""" 
Printing the results of the analysis
"""

puts "~~~~~~~~~~~~~"

puts "Person 1 Name: #{person_list[0][:name]}, Messages sent: #{person_list[0][:message_count]}, Words sent: #{person_list[0][:word_count]} "

puts "~~"

puts "Person 2 Name: #{person_list[1][:name]}, Messages sent: #{person_list[1][:message_count]}, Words sent: #{person_list[1][:word_count]} "

puts "~~"

puts "Both of you have spent atleast #{statistics[:minutes_count]} minutes in this conversation."

start_date = DateTime.parse(messages_array[0][:time])
end_date = DateTime.parse(messages_array[-1][:time])

total_days = (end_date - start_date).to_i + 1

puts "~~"

puts "Start Date: #{start_date.strftime("%d/%m/%Y")}"
puts "End Date: #{end_date.strftime("%d/%m/%Y")}"
puts "Total Days: #{total_days}"

puts "Unique Days: #{statistics[:unique_days]}"

puts "~~"

puts "There were #{total_days - statistics[:unique_days]} full days without any conversation and they were divided as follows: #{messages_gap}"

puts "~~~~~~~~~~~~~"

