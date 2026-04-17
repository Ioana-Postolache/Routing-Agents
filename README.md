# Retail Intelligence System

This project demonstrates a simple retail intelligence system built with multiple LLM-powered agents in Python.

The system routes retail-related user queries to the appropriate specialist agent. For pricing questions, it follows a multi-step workflow by first gathering product research and customer analysis, then using that information to generate a pricing recommendation.

## Overview

The goal of this project is to build a routing-based agent system that can handle different types of retail queries.

The system supports three main task types:

- product research
- customer analysis
- pricing strategy

A routing agent first classifies the user’s query, then dispatches it to the correct specialist. If the query is about pricing strategy, the router gathers prerequisite information from other agents before calling the pricing strategist.

## Agents

### 1. Product Researcher Agent

This agent handles product-related research tasks.

It may answer questions about:

- product specifications
- market trends
- competitor pricing
- product positioning

### 2. Customer Analyzer Agent

This agent handles customer-related analysis tasks.

It may answer questions about:

- customer feedback
- customer preferences
- buying behavior
- purchase patterns

### 3. Pricing Strategist Agent

**Function:** `pricing_strategist_agent(query, product_data=None, customer_data=None)`

This agent recommends pricing strategies based on:

- the original pricing query
- product research data
- customer analysis data

Its job is to suggest an optimal price or price range and explain the reasoning behind the recommendation.

### 4. Routing Agent

**Function:** `routing_agent(query)`

This is the core controller of the system.

It uses an LLM to classify the user’s query into one of three categories:

- `product research`
- `customer analysis`
- `pricing strategy`

Based on the classification, it routes the query to the correct agent.

For pricing strategy queries, it performs a multi-step workflow:

1. call the product researcher agent
2. call the customer analyzer agent
3. pass both outputs into the pricing strategist agent

## Workflow

The system follows this logic:

- If the query is about product research, route directly to the product researcher.
- If the query is about customer analysis, route directly to the customer analyzer.
- If the query is about pricing strategy:
  - gather product research
  - gather customer analysis
  - generate a final pricing recommendation

This design shows how routing can be used to coordinate multiple specialized agents.

## Example Query Types

Examples of supported queries include:

- "What are the latest trends in skincare products?"
- "What do customers think about eco-friendly packaging?"
- "What price should we set for our new skincare line?"

## Project Goals

This exercise helps demonstrate how to:

- build specialized LLM agents in Python
- classify user queries with an LLM
- route tasks dynamically based on query type
- chain multiple agent calls together for more complex tasks
- design prompts for structured multi-agent workflows

## How to run


```python starter.py```
