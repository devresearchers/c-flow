# Claude Flow Automation Features

## Overview

The Claude Flow automation system provides intelligent workflow orchestration with MLE-STAR (Machine Learning Engineering via Search and Targeted Refinement) methodology as the flagship example. This system allows you to execute complex, multi-agent workflows with Claude CLI integration for actual code execution.

## Key Features

- **MLE-STAR Methodology**: Complete ML engineering workflow from search to deployment
- **Claude CLI Integration**: Spawn real Claude Code instances for actual execution
- **Modular Architecture**: Preserves existing swarm and hive-mind functionality
- **Non-Interactive Mode**: Perfect for CI/CD integration
- **Workflow Templates**: JSON-based workflow definitions with dependency management
- **Agent Coordination**: Full hooks integration for cross-agent coordination

## Commands

### 1. MLE-STAR Workflow (Flagship)

The MLE-STAR command runs the complete Machine Learning Engineering workflow:

```bash
# Basic MLE-STAR execution
claude-flow automation mle-star --dataset data/train.csv --target price --claude

# Advanced configuration
claude-flow automation mle-star \
  --dataset sales.csv \
  --target revenue \
  --output models/sales/ \
  --name "sales-prediction" \
  --search-iterations 5 \
  --refinement-iterations 8 \
  --max-agents 6 \
  --claude
```

#### MLE-STAR Options

- `--claude`: Enable Claude CLI integration (recommended)
- `--dataset <path>`: Path to dataset file (default: ./data/dataset.csv)
- `--target <column>`: Target column name (default: target)
- `--output <dir>`: Model output directory (default: ./models/)
- `--name <experiment>`: Experiment name for tracking
- `--search-iterations <n>`: Web search iterations (default: 3)
- `--refinement-iterations <n>`: Refinement cycles (default: 5)
- `--max-agents <n>`: Maximum agents to spawn (default: 6)
- `--non-interactive`: Run without user prompts
- `--no-claude-warning`: Suppress Claude integration warnings

### 2. Custom Workflow Execution

Execute any JSON/YAML workflow file:

```bash
# Execute custom workflow
claude-flow automation run-workflow my-workflow.json --claude --non-interactive

# With variable overrides
claude-flow automation run-workflow workflow.json \
  --claude \
  --variables '{"dataset_path": "data/custom.csv", "target_column": "sales"}' \
  --max-concurrency 5 \
  --timeout 7200000
```

#### Run-Workflow Options

- `--claude`: Enable Claude CLI integration for actual execution
- `--non-interactive`: Run in non-interactive mode (no prompts)
- `--output-format <format>`: Output format (text, json)
- `--variables <json>`: Override workflow variables (JSON format)
- `--max-concurrency <n>`: Maximum concurrent tasks (default: 3)
- `--timeout <ms>`: Execution timeout in milliseconds
- `--verbose`: Enable detailed logging

### 3. Legacy Commands (Preserved)

All existing automation commands are preserved:

```bash
# Auto-spawn agents based on complexity
claude-flow automation auto-agent --task-complexity enterprise

# Smart agent spawning
claude-flow automation smart-spawn --requirement "web-development" --max-agents 8

# Workflow selection
claude-flow automation workflow-select --project-type api --priority speed
```

## Workflow Definition Format

### Basic Structure

```json
{
  "name": "My Workflow",
  "version": "1.0.0",
  "description": "Workflow description",
  "variables": {
    "dataset_path": "data/dataset.csv",
    "target_column": "target"
  },
  "agents": [
    {
      "id": "researcher",
      "type": "researcher",
      "name": "Research Agent",
      "config": {
        "capabilities": ["web_search", "data_analysis"],
        "search_depth": "comprehensive"
      }
    }
  ],
  "tasks": [
    {
      "id": "research_task",
      "name": "Research ML Approaches",
      "type": "research",
      "description": "Search for state-of-the-art ML approaches",
      "assignTo": "researcher",
      "timeout": 900,
      "input": {
        "problem_type": "${dataset_analysis.problem_type}"
      },
      "output": {
        "recommended_approaches": "array"
      }
    }
  ],
  "dependencies": {
    "research_task": []
  },
  "settings": {
    "maxConcurrency": 3,
    "timeout": 7200,
    "failurePolicy": "continue"
  }
}
```

### Agent Types

- `researcher`: Web search and analysis
- `coder`: Code implementation
- `optimizer`: Performance optimization
- `architect`: System design
- `tester`: Quality assurance
- `coordinator`: Workflow orchestration

### Task Dependencies

Define task execution order:

```json
"dependencies": {
  "task_b": ["task_a"],
  "task_c": ["task_a", "task_b"],
  "task_d": ["task_c"]
}
```

### Variable Substitution

Use `${variable_name}` syntax for dynamic values:

```json
"input": {
  "dataset_path": "${dataset_path}",
  "target": "${target_column}",
  "previous_result": "${previous_task.output.result}"
}
```

## Examples

### Example 1: Simple ML Pipeline

```json
{
  "name": "Simple ML Pipeline",
  "agents": [
    {
      "id": "data_scientist",
      "type": "coder",
      "name": "Data Scientist",
      "config": {
        "capabilities": ["python", "scikit-learn", "pandas"]
      }
    }
  ],
  "tasks": [
    {
      "id": "data_prep",
      "name": "Data Preparation",
      "assignTo": "data_scientist",
      "description": "Load and preprocess data"
    },
    {
      "id": "model_train",
      "name": "Model Training",
      "assignTo": "data_scientist", 
      "depends": ["data_prep"],
      "description": "Train ML model"
    }
  ]
}
```

### Example 2: Multi-Agent Research

```json
{
  "name": "Research Project",
  "agents": [
    {
      "id": "researcher1",
      "type": "researcher",
      "name": "Primary Researcher"
    },
    {
      "id": "analyst",
      "type": "analyst", 
      "name": "Data Analyst"
    }
  ],
  "tasks": [
    {
      "id": "literature_review",
      "assignTo": "researcher1",
      "description": "Review existing literature"
    },
    {
      "id": "data_analysis",
      "assignTo": "analyst",
      "depends": ["literature_review"],
      "description": "Analyze research data"
    }
  ]
}
```

## Claude CLI Integration

When `--claude` flag is used:

1. **Agent Spawning**: Real Claude Code instances are spawned for each agent
2. **Coordination**: Agents use claude-flow hooks for synchronization
3. **Memory Sharing**: Cross-agent coordination through memory system
4. **Actual Execution**: Real file operations and code generation

### Agent Coordination Protocol

Each agent automatically uses:

```bash
# Before starting work
npx claude-flow@alpha hooks pre-task --description "task description"

# After each file operation  
npx claude-flow@alpha hooks post-edit --file "filename"

# Store findings
npx claude-flow@alpha memory store "agent/results" "findings"

# When complete
npx claude-flow@alpha hooks post-task --task-id "task-id"
```

## Non-Interactive Mode

Perfect for CI/CD integration:

```bash
# CI/CD pipeline example
claude-flow automation mle-star \
  --dataset $DATASET_PATH \
  --target $TARGET_COLUMN \
  --claude \
  --non-interactive \
  --output $OUTPUT_DIR \
  --name "$BUILD_ID-experiment"
```

## Error Handling

### Failure Policies

- `continue`: Continue with remaining tasks if one fails
- `fail-fast`: Stop execution on first failure

### Retry Configuration

```json
"tasks": [
  {
    "id": "task1",
    "retries": 3,
    "timeout": 1800,
    "description": "Task with retry logic"
  }
]
```

## Performance Optimization

### Concurrency Control

```json
"settings": {
  "maxConcurrency": 5,  // Max parallel tasks
  "timeout": 3600000,   // 1 hour timeout
  "failurePolicy": "continue"
}
```

### Agent Optimization

- Use appropriate agent counts (3-8 for most workflows)
- Balance parallel vs sequential execution
- Optimize timeout values based on task complexity

## Best Practices

1. **Start Small**: Begin with simple workflows and expand
2. **Use Claude Integration**: Enable `--claude` for actual execution
3. **Test Workflows**: Validate workflow definitions before production
4. **Monitor Progress**: Use verbose logging for debugging
5. **Handle Failures**: Design workflows with appropriate retry logic
6. **Document Variables**: Clearly define all workflow variables

## Integration with Existing Systems

The automation system preserves all existing functionality:

- **Swarm Commands**: Full compatibility with `claude-flow swarm`
- **Hive-Mind**: Complete integration with `claude-flow hive-mind`
- **Memory System**: Shared memory across all components
- **Hooks System**: Full lifecycle management integration

## Troubleshooting

### Common Issues

1. **Claude CLI Not Found**: Install Claude Code from https://claude.ai/code
2. **Workflow Validation Errors**: Check JSON syntax and required fields
3. **Agent Spawn Failures**: Verify system resources and permissions
4. **Timeout Issues**: Increase timeout values for complex tasks

### Debug Mode

```bash
claude-flow automation mle-star --verbose --claude
```

### Log Analysis

Check logs for detailed execution information:
- Agent coordination messages
- Task execution progress
- Error details and stack traces

## Future Enhancements

Planned features:
- YAML workflow support
- Visual workflow designer
- Template marketplace
- Advanced analytics dashboard
- Integration with external ML platforms

---

For more information, see:
- [MLE-STAR Methodology](https://github.com/ruvnet/claude-code-flow/docs/mle-star.md)
- [Workflow Examples](https://github.com/ruvnet/claude-code-flow/examples/workflows/)
- [API Reference](https://github.com/ruvnet/claude-code-flow/docs/api-reference.md)