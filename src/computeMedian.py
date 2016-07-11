import sys
import re
import os
import datetime
import json
import time
import dateutil.parser
import graph

class MedianPayment:
    def __init__(self, file_in, file_out, enableLogging):
        self.file_in = file_in
        self.file_out = file_out
        self.TIME_INTERVAL = 60
        self.LOG = enableLogging
        self.g = graph.Graph()
        self.array = []
        self.maxTimestamp = 0
        self.log_file = None
    

    def getDateTimeFromISO8601String(self, s):
        d = dateutil.parser.parse(s)
        return d
    
    def addPayment(self, actor, target, timestamp):
        if self.LOG:
            self.log_file.write('processing payment ( %s , %s, %3d)\n'  % ( actor, target, timestamp))
        if (timestamp<self.maxTimestamp):
            if (self.maxTimestamp-timestamp<self.TIME_INTERVAL):
                if self.LOG:
                    self.log_file.write('new edge added within maxTimestamp %d\n' % self.maxTimestamp )
                self.g.add_edge(actor, target, timestamp)
            else:
                if self.LOG:
                    self.log_file.write('payment ignored because it falls outside of %d time interval\n' % self.TIME_INTERVAL)
        else:
            self.maxTimestamp = timestamp
            for v in self.g:
                for w in v.get_connections():
                    vid = v.get_id()
                    wid = w.get_id()
                    if (self.maxTimestamp-v.get_weight(w) >=self.TIME_INTERVAL):
                        if self.LOG:
                            self.log_file.write('removing outdated edge ( %s , %s, %d)\n'  % ( vid, wid, v.get_weight(w)))
                        self.g.remove_edge(vid, wid)
            if self.LOG:
                self.log_file.write('new edge added with new maxTimestamp %d\n' % self.maxTimestamp )
            self.g.add_edge(actor, target, timestamp)
    
    def processPayments(self):

        #create and open the log file that contains the intermediate debug information
        if self.LOG:
            self.log_file = open('log_file.txt', 'w+')
        p='%Y-%m-%dT%H:%M:%SZ'
        line_num = 0
        for line in self.file_in:
            if self.LOG:
                line_num = line_num + 1
                self.log_file.write('\nline_num = %d\n' % line_num)
        
            try:
                json_str = json.loads(line)
            
                timestamp =  int(time.mktime(time.strptime(json_str.values()[0],p)))
                actor = json_str.values()[1]
                target = json_str.values()[2]
            
                self.addPayment(actor, target, timestamp)
                median = self.g.computeMedianDegree()
                    
                if self.LOG:
                    self.log_file.write( 'Median is %.02f\n' % median)
                
                self.file_out.write('%.02f\n' % median)
            
        
            except (ValueError,IndexError):  # includes simplejson.decoder.JSONDecodeError
                if self.LOG:
                    self.log_file.write('ERROR: Decoding JSON has failed')
        if self.LOG:
            self.log_file.close()

def main():
    args = sys.argv[1:]
    
    #Provide the usage of the command
    if not args:
        print 'usage: input_file output_file '
        sys.exit(1)
    
    #open input file for reading the payment strings
    file_in = open(args[0], 'rU')
    #create and open the output file that contains the rolling medians
    file_out = open(args[1], 'w+')

    mp = MedianPayment(file_in, file_out, True);
    mp.processPayments();

    file_in.close()
    file_out.close()

if __name__ == '__main__':
    main()
