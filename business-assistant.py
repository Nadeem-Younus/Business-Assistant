from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

client =   OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Tools

import json

# Complete Calculator with Error Handling.
def calculate_safe(expression):
    try:
        expression = str(expression)
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"success": True, "result": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def web_search(query):
    results = {
        "ai trends": "Latest AI: Advanced reasoning, multimodal models",
        "technology": "Tech news: AI adoption accelerating",
        "email tips": "Email tips: Clear subject, concise content"
    }
    for keyword in results:
        if keyword in query.lower():
            return json.dumps({"results": results[keyword]})
    return json.dumps({"results": f"Info about {query}"})

def web_search(query):
    """ Mock web search for business info """
    # Mock data - replace with real API if desired
    mock_results = {
        " market trends ": " Tech sector showing 15% growth in Q1 2026",
        " industry news ": "AI adoption increasing across all sectors",
        " best practices ": " Email best practices : personalization , clear CTAs",
        " competitor ": " Main competitors expanding to new markets"
    }
    
    for keyword in mock_results:
        if keyword in query . lower ():
            return json . dumps ({" results ": mock_results [ keyword ]})
        
    return json . dumps ({" results ": f" Information about { query }"})


def analyze_data(data_string, operation):
    """ Analyze business data """
    try:
        data = json.loads(data_string)
        # Handle list format
        if isinstance(data, list):
            values = [float (x) for x in data]
        # Handle dictionary format (e.g., {" Jan ": 50000 , " Feb ": 60000})
        elif isinstance(data, dict):
            values = [float (v) for v in data.values()]
        else:
            return json.dumps ({"error": "Invalid data format"})
        if operation == "sum":
            result = sum(values)
        elif operation == "average":
            result = sum(values)/len(values)
        elif operation == "max":
            result = max(values)
        elif operation == "min":
            result = min(values)
        else :
            return json.dumps({"error": "Unknown operation"})    
        return json.dumps({
            " result ": result ,
            " count ": len ( values )
        })
    except Exception as e:
        return json . dumps ({" error ": str(e)})


def format_report(report_type, data, period):
    """ Format business report with structure """
    template = {
        "sales": {
            "sections": ["Executive Summary", "Key Metrics", "Analysis ", "Recommendations"],
            " header": f"{period} Sales Performance Report "
        },
        " quarterly": {
            "sections": ["Overview", "Financial Highlights", "Operational Updates", "Next Steps"],
            "header": f"{period} Quarterly Report "
        }
    }
    report_template = template.get(report_type, template["sales"])
    
    return json . dumps ({
        "header": report_template["header"],
        "sections": report_template["sections"],
        "timestamp": datetime.now().strftime("%B %d, %Y")
    })



# Tool schemas
calculator_tool = {"type": "function", "function": {"name": "calculate", "description": "Calculate financial metrics , percentages , growth rates", "parameters": {"type": "object", "properties": {"expression": {"type": "string", "description": "Math expression like '50000 * 0.15 ' or '(75 -50) /50*100 '"}}, "required": ["expression"]}}}
web_search_tool = {"type": "function", "function": {"name": "web_search", "description": "Search web", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}
data_analyzer_tool = {"type": "function", "function": {"name": "analyze_data", "description": "Analyze data", "parameters": {"type": "object", "properties": {"data_string": {"type": "string"}, "operation": {"type": "string", "enum": ["sum", "average", "max", "min"]}}, "required": ["data_string", "operation"]}}}
report_formatter_tool = {"type": "function", "function": {"name": "format_report", "description": "Format business reports", "parameters": {"type": "object", "properties": {"report_type": {"type": "string", "enum": ["sales", "quarterly"]}, "data": {"type": "string"}, "period": {"type": "string"}}, "required": ["report_type", "data", "period"]}}}


############## EnhancedEmailWriter class ################

class EnhancedEmailWriter:
    """
    COMPLETE email writer that can research topics.
    """
    
    def __init__(self):
        self.tools = [web_search_tool]
        self.functions = {"web_search": web_search}
    
    def write(self, description, tone="professional"):
        print(f"\n📧 Writing email: {description}")
        print(f"   Tone: {tone}\n")
        
        system_prompt = f"""You are a professional email writer.
        Write in a {tone} tone.
        Adapt writing style based on recipient type:
            - client → polite and relationship-focused
            - team → collaborative and clear
            - stakeholder → executive and concise
            - supplier → professional and operational
        Tone rules:
            - casual: friendly, simple, conversational
            - professional: business-like, clear, structured
            - formal: strict, respectful, corporate language
        
        STRICT OUTPUT FORMAT (must follow exactly):
        Subject: <one line subject>
        Greeting: <greeting line>
        Body:
        <multi-line email body with proper paragraphs>
        Closing:
        <professional closing line>
        If you need current information, use web_search.
        Include subject, greeting, body, closing."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write email: {description}"}
        ]
        
        # First API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools
        )
        
        response_message = response.choices[0].message
        
        # Check if AI wants to research
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔍 Researching: {function_args.get('query', 'N/A')}")
                
                result = self.functions[function_name](**function_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final email with research
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            
            return final_response.choices[0].message.content
        
        return response_message.content

    

############# SmartSummarizer class ###########
"""COMPLETE summarizer with analytics."""
class SmartSummarizer:
    """
    COMPLETE summarizer with detailed analytics.
    """
    
    def summarize(self, text, style="short"):
        print(f"\n📝 Summarizing ({style} style)...\n")
        
        # Analytics
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        # Style instructions
        styles = {
            "short": "1-2 sentences",
            "medium": "A paragraph (3-4 sentences)",
            "detailed": "Multiple paragraphs"
        }
        
        # Get summary
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Summarize as {styles.get(style, styles['short'])}"},
                {"role": "user", "content": f"Summarize:\n{text}"}
            ],
            temperature=0.3
        )
        
    
        summary = response.choices[0].message.content
        summary_words = len(summary.split())
        reduction = ((word_count - summary_words) / word_count * 100)
        
        
        # Display
        print("=" * 70)
        print("📊 SUMMARY ANALYSIS")
        print("=" * 70)
        print(f"Original: {word_count} words, ~{sentence_count} sentences")
        print(f"Summary: {summary_words} words")
        print(f"Reduction: {reduction:.1f}%")
        print(f"Style: {style.title()}")
        #print()
        print("-" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(summary)
        print("-" * 70)

        return summary
    

########## MultiToolAssistant class ##########

import json

class MultiToolAssistant:
    """
    COMPLETE assistant with all tools.
    Tracks usage and handles errors.
    """
    
    def __init__(self):
        self.tools = [calculator_tool, web_search_tool, data_analyzer_tool]
        self.functions = {
            "calculate": calculate_safe,
            "web_search": web_search,
            "analyze_data": analyze_data
        }
        self.tool_usage = {name: 0 for name in self.functions.keys()}
    
    def ask(self, question):
        """Ask a question and get answer (using tools if needed)"""
        print(f"❓ Question: {question}\n")
        
        messages = [{"role": "user", "content": question}]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools
        )
        
        response_message = response.choices[0].message
        
        if not response_message.tool_calls:
            return response_message.content
        
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Track usage
            self.tool_usage[function_name] += 1
            
            print(f"🔧 Using {function_name}...")
            
            result = self.functions[function_name](**function_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        print()
        return final_response.choices[0].message.content
    
    def stats(self):
        """Show usage statistics"""
        print("\n📊 Tool Usage Statistics:")
        print("=" * 40)
        for tool, count in self.tool_usage.items():
            print(f"  {tool}: {count} calls")
        print("=" * 40)



########### Main Class that manages all features ###########

class BusinessAssistant :
    """
    Main business assistant class
    """
    
    def __init__ (self):
        # Initialize all tools
        self.tools = [calculator_tool, web_search_tool, data_analyzer_tool, report_formatter_tool]
        
        self.functions = {
        "calculate": calculate_safe,
        "web_search": web_search,
        "analyze_data": analyze_data,
        "format_report": format_report
        }
        self.email_writer = EnhancedEmailWriter()
        self.summarizer = SmartSummarizer()

        print("=" * 77)
        print("✅ Business Assistant initialized!")
        print("   Features:\n    Professional emails with research\n    Business reports from data\n    Analyze sales/revenue data\n    Meeting summaries\n    Draft client communications\n")
        print("=" * 77)
    
    def parse_email_intent(self, request):
        text = request.lower()

        # -------------------
        # Recipient detection
        # -------------------
        if "client" in text:
            recipient_type = "client"
        elif "team" in text:
            recipient_type = "team"
        elif "stakeholder" in text:
            recipient_type = "stakeholder"
        elif "supplier" in text:
            recipient_type = "supplier"
        else:
            recipient_type = "stakeholder"  # default

        # -------------
        # Tone detection
        # -------------
        if "formal" in text:
            tone = "formal"
        elif "friendly" in text:
            tone = "friendly"
        else:   
            tone = "professional"  # default

        return recipient_type, tone

    def parse_report_intent(self, text):
        text = text.lower()

        if "casual" in text:
            tone = "casual"
        elif "friendly" in text:
            tone = "friendly"
        else:
            tone = "formal"

        return tone

    def process_request(self, request):
        """Main router like MultiCapabilityAssistant"""

        request_lower = request.lower()

        print("\n" + "=" * 60)
        print("📥 BUSINESS REQUEST")
        print("=" * 60)
        print(request)

        # 1. EMAIL
        if any(word in request_lower for word in ["email", "write email", "compose"]):
            return self.write_email(
                purpose=request,
                recipient_type="stakeholder",
                tone="professional"
            )
        # 2. REPORT
        elif any(word in request_lower for word in ["report", "generate report"]):
            return self.generate_report(
                report_type="business",
                data=request,
                period="current"            )
        # 3. DATA ANALYSIS
        elif any(word in request_lower for word in ["analyze", "sales", "revenue", "data"]):
            return self.analyze_business_data(
                query=request,
                data=request
            )
        # 4. MEETING SUMMARY
        elif any(word in request_lower for word in ["meeting", "summarize meeting", "minutes"]):
            return self.summarize_meeting(
                notes=request,
                date="today"
            )
        # DEFAULT (fallback to email-style assistant)
        else:
            return self.write_email(
                purpose=request,
                recipient_type="stakeholder",
                tone="professional"
            )

    def write_email(self, purpose, recipient_type="Professional", tone="Formal", research_topic=None):
        """
        Feature 1: Professional Business Email Writer
        """

        print("\n📧 BUSINESS EMAIL WRITER")
        print("=" * 60)
        print(f"Recipient Type: {recipient_type}")
        print(f"Tone: {tone}")

        # Build detailed email request
        description = f"""
        Write a business email.

        Email Purpose:
        {purpose}

        Recipient Type:
        {recipient_type}

        Tone:
        {tone}
        """

        # Optional research
        if research_topic:
            description += f"""

            Include recent information about:
            {research_topic}
            """

        # Reuse EnhancedEmailWriter
        email = self.email_writer.write(description, tone)

        return email
        #pass

    def generate_report(self, report_type, data, period):
        try:
            print("\n📊 BUSINESS REPORT GENERATOR")
            print("=" * 60)

            prompt = f"""
            Write a {report_type} report in a {period} tone style.

            Topic:
            {data}

            Include:
            - Executive summary
            - Key insights
            - Progress overview
            - Recommendations
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a business analyst."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Report generation failed: {str(e)}"
    
    def summarize_meeting(self, notes, date, attendees=None):
        """ Feature 3: Meeting summarizer """

        print("\n📝 MEETING SUMMARY")
        print("=" * 60)

        full_text = f"""
        Meeting Date: {date}
        Attendees: {attendees if attendees else 'Not specified'}

        Notes:
        {notes}
        """

        # Reuse existing summarizer
        return self.summarizer.summarize(full_text, style="short")
    
    def analyze_business_data(self, query, data):
        """ Feature 4: Data analyzer """

        print("\n📈 BUSINESS DATA ANALYSIS")
        print("=" * 60)

        # default operation detection
        query_lower = query.lower()

        if "average" in query_lower:
            operation = "average"
        elif "sum" in query_lower:
            operation = "sum"
        elif "max" in query_lower:
            operation = "max"
        elif "min" in query_lower:
            operation = "min"
        else:
            operation = "average"

        #result = analyze_data(json.dumps(data), operation)
        return "Please provide numeric JSON data like [100,200,300]"
        return result

    
    def draft_client_communication(self, comm_type, client, context, tone):
        """ Feature 5: Client communication """

        print("\n🤝 CLIENT COMMUNICATION")
        print("=" * 60)

        purpose = f"""
        Type: {comm_type}
        Client: {client}
        Context: {context}
        """
        return self.email_writer.write(purpose, tone)


assistant = BusinessAssistant()

'''assistant.write_email(
    purpose="announce AI dashboard launch", 
    recipient_type="stakeholder",
    tone="formal",
    research_topic=None
    )
'''

while True:
    user_input = input("\n💬 Enter request (or 'exit'): ")

    if user_input.lower() == "exit":
        break

    response = assistant.process_request(user_input)
    print("\n🤖 RESPONSE:\n", response)

