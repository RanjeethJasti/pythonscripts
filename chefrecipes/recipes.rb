default.rb 
----------

package "apache2" do  
  action :install 
end

service "apache2" do
   action [:start, :enable] 
end 

cookbook_file "/var/www/index.html" do
  source "index.html"
  mode "0644"
end


cookbook_file
-------------

files/default/index.html

<html>
<body>
<h1> Hello world </h1>
</body>
</html>

template files
--------------

template "/var/www/html/index.html" do
  source "index.html.erb"
  mode "0644"
end

templates/default/index.html.erb

<h1> Hello world! </h1>
<p> My Name is <%=node['hostname']%>. </p>



cross-platform

package_name = "apache2"
service_name = "apache2"
document_root = "/var/www/"

if node["platform"] == "centos"
 package_name = "httpd"
 service_name = "httpd"
 document_root = "/var/www/html"
end

package package_name do  
  action :install 
end

service service_name do
   action [:start, :enable] 
end

cookbook_file "#{document_root}/index.html" do
  source "index.html"
  mode "0644"
end


Attributes

attributes/default.rb

default["document_root"] = "/var/www/html"

case node["platform"] 
when "ubuntu"
  default["package_name"] = "apache2"
  default[“service_name”] = "apache2"
when "centos"
  default["package_name"] = "httpd"
  default["service_name"] = "httpd"
end


recipe

package node["package_name"] do  
  action :install 
end

service node["service_name"] do
   action [:start, :enable] 
end

cookbook_file "#{node["document_root"]}/index.html" do
  source "index.html"
  mode "0644"
end


>> Environment

vi environment/development.rb

name "development"
description "For development"
cookbook "apache", "=0.2.0"


vi environment/production.rb

name "production"
description "For production"
cookbook "apache", "=0.1.1"

knife environment from file development.rb
knife environment from file production.rb

knife environment list

Libraries


class Chef
  class Recipe
    class PlatformUtils
  
def self.send_email(opts={})        
            
        require 'net/smtp'   
        subject         = opts[:subject]
        emailbody       = opts[:body]
        to_addr         = opts[:to_addr]
        from_addr       = opts[:from_addr]
        #opts[:to] ||= node['partners']['mail']['to']
        marker = "AUNIQUEMARKER"

        # Define the main headers.
emailsubject =<<EOF
Subject: #{subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=#{marker}

--#{marker}
EOF

# Define the message action
emailcontent =<<EOF
#Content-Type: 8bit
Content-Transfer-Encoding:8bit
#{emailbody}
--#{marker}
EOF

      mailtext = emailsubject + emailcontent 
      Chef::Log.info("sending error email to: #{to_addr}")
      Net::SMTP.start("localhost", 25) do |smtp|
         smtp.send_message mailtext, from_addr, to_addr
      end
end

end
end
end


Recipe

bash 'Test code' do
    user 'vagrant'
    group 'vagrant'
    code <<-EOH
    cat /dev/null > /tmp/service-logic.log
    echo "ERROR: This is a test error line" > /tmp/service-logic.lo
    EOH
end

ruby_block 'sendemail' do
        block do
                

errors = File.readlines("/tmp/service-logic.log").select { |line| line =~ /ERROR/ }
name = node.name
subject = "Chef client ecountered errors on #{name}"
from_addr = "mai@#{name}"
to_addr = "mail2josephthomas@gmail.com"
        unless errors.empty?
                PlatformUtils.send_email( :body => errors.join("\n"),
                                        :subject => subject,
                                        :from_addr => from_addr,
                                        :to_addr => to_addr)
        end
        end
end



>> URL test

#
# Cookbook:: testurl
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
node["partners"].each do |name,partner|

ruby_block "URL validation for partner #{partner}" do
    require "uri"
    block do
            begin
                site = partner['url']
            rescue
                puts "\n\e [33m[WARNING] Skipping test - partner #{name} has no url attribute \e[0m"
            end
            if (site != 'nil') || (site != '')
                site.to_s.split(" ").each  do |url|
                begin
                    uri = URI.parse(url)
                    if uri.host.nil? && uri.port.nil?
                        puts "\n\e[31m[ERROR] URL is not in proper format for partner #{name} - (#{site}) \e[0m"
                    else
                    puts "\n[SUCCESS] URL is valid for partner #{name} - (#{site})"
                    end
                rescue
                    puts "\n\e[31m[ERROR] URL is not in proper format for partner #{name} - (#{site}) \e[0m"
                end
            end
            else
                puts "\n\e[31m[ERROR] URL is empty for partner #{partner} \e[0m"
            end
    end
end
end

node["partners"].each do |name,partner|

ruby_block "Check connectivity to #{name} partner" do
    require "socket"
    require "uri"
    require 'timeout'
    block do
            begin
                site = partner['url']
            rescue
                puts "\n\e[33m[WARNING] Skipping test - partner #{name} has no url attribute \e[0m"
            end
            if (site != 'nil') || (site != '')
            site.to_s.split(" ").each  do |url|
            begin
                uri = URI.parse(url)
            rescue
                puts "\n\e[31m[ERROR] Invalid URL \e[0m"
            end            
            if ! url.start_with?('http', 'https')
                begin
                parseurl = url.split(':')
                if parseurl.length == 1
                   uri.host = parseurl[0].to_s
                elsif parseurl.length == 2
                   newurl = "http://" + url.to_s
                   uri = URI(newurl)
                end
                rescue
                 puts "\n\e[31m[ERROR] Invalid URL format for #{name}  "
                end
            end
            if ! uri.host.nil? and uri.port.nil?
                   pingresult=system('ping', '-c 3', uri.host )
                   if pingresult
                      puts "[SUCCESS] Ping is success for #{name} - #{url}"
                   else
                      puts "\n\e[31m[ERROR] Ping failed for #{name} - #{url}\e[0m"
                   end

            else
                begin
                    Timeout::timeout(1) do
                    begin
                        s = TCPSocket.new(uri.host, uri.port)
                        s.close
                        puts "[SUCCESS] Connection is active for #{name} - #{url}"
                    rescue Exception => ex
                        puts "\n\e[31m[ERROR] Connection failed for #{name} - #{url} #{ex.message} \e[0m"
                    end
                    end
                rescue Timeout::Error
                    puts "\n\e[31m[ERROR] Connection timed out for #{name} - #{url}\e[0m"
                end
            end
        end
    end         
    end
end
end


Env json file

{
  "name": "development",
  "description": "Development Environment",
  "override_attributes": {
    "partners": {
      "facebook": {
        "url": "http://facebook.com:80"
      },
      "facebooksecure": {
        "url": "https://facebook.com:443"
      },
      "wrongurl": {
        "url": "https://facebook.com:25443"
      },
      "ip": {
        "url": "192.168.33.43"
        }
     }
  }
}