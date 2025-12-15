Use Cases
=========

Shepherd MCP enables powerful debugging and analysis workflows for AI agents. 
Here are common use cases with example prompts.

.. contents:: On this page
   :local:
   :depth: 2

Debugging Failed Runs
---------------------

Quickly identify and investigate sessions with errors.

**AIOBS:**

.. code-block:: text

   "Show me all AIOBS sessions that had errors in the last 24 hours"
   
   "Find AIOBS sessions with failed evaluations from today"
   
   "Get the details of the most recent AIOBS session with errors"

**Langfuse:**

.. code-block:: text

   "List Langfuse traces with errors from yesterday"
   
   "Find Langfuse observations with WARNING or ERROR level"

Performance Analysis
--------------------

Analyze and compare session performance metrics.

**Compare Sessions:**

.. code-block:: text

   "Compare AIOBS session abc123 with session def456 and tell me 
   which one was more efficient"
   
   "Show me the token usage difference between these two sessions"

**Latency Analysis:**

.. code-block:: text

   "What was the average latency for LLM calls in my last AIOBS session?"
   
   "Find Langfuse traces with latency over 5 seconds"

Prompt Regression Detection
---------------------------

Identify changes in prompts and their effects.

**System Prompts:**

.. code-block:: text

   "Compare the system prompts between AIOBS sessions abc123 and def456"
   
   "Show me all unique system prompts used in my AIOBS sessions today"

**Evaluation Tracking:**

.. code-block:: text

   "Find Langfuse traces with failed evaluations"
   
   "Show me the evaluation pass rate trend for my AIOBS sessions"

Cost Tracking
-------------

Monitor and analyze LLM usage costs.

**Token Usage:**

.. code-block:: text

   "What's the total token usage for my AIOBS sessions this week?"
   
   "List Langfuse observations and summarize the total cost"

**Cost Comparison:**

.. code-block:: text

   "Compare the token costs between AIOBS sessions abc and def"
   
   "Find Langfuse traces with cost over $0.10"

Session Inspection
------------------

Deep dive into individual sessions.

**Trace Trees:**

.. code-block:: text

   "Get the full trace tree for the most recent Langfuse trace and 
   explain what happened"
   
   "Show me the function call hierarchy for AIOBS session abc123"

**Detailed Analysis:**

.. code-block:: text

   "What models were used in AIOBS session abc123?"
   
   "Show me all tool calls made during Langfuse trace xyz"

Cross-Provider Analysis
-----------------------

Analyze data from multiple observability providers.

.. code-block:: text

   "Show me both AIOBS sessions and Langfuse traces from today"
   
   "Compare the number of LLM calls between AIOBS and Langfuse 
   for my recent runs"

Model Usage Analysis
--------------------

Track which models are being used across your agents.

**Provider Distribution:**

.. code-block:: text

   "What LLM providers were used in my AIOBS sessions this week?"
   
   "Show me the model distribution for Langfuse traces from production"

**Model Comparison:**

.. code-block:: text

   "Find AIOBS sessions that used gpt-4o-mini"
   
   "List all Langfuse observations using Claude models"

Function Call Analysis
----------------------

Analyze function/tool usage in your agents.

**AIOBS Function Events:**

.. code-block:: text

   "What functions were called in AIOBS session abc123?"
   
   "Find AIOBS sessions that called the 'search' function"

**Tool Usage:**

.. code-block:: text

   "Show me which tools were used across my AIOBS sessions today"
   
   "Compare tool usage between two sessions"

Label-Based Filtering
---------------------

Use labels to organize and filter sessions.

.. code-block:: text

   "Find all AIOBS sessions with label environment=production"
   
   "Show me AIOBS sessions labeled with user_type=premium"

Date Range Queries
------------------

Filter sessions by time periods.

**Specific Dates:**

.. code-block:: text

   "List AIOBS sessions from 2024-01-15"
   
   "Show Langfuse traces between 2024-01-01 and 2024-01-31"

**Relative Time:**

.. code-block:: text

   "Find AIOBS sessions from the last hour"
   
   "Show me Langfuse sessions from this week"

