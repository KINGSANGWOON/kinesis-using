# Kinesis Data Analytics Options

## Scaling
### Parallelism
- specify the number of parallel tasks
- Minimum: 1, Maximum: service limit

### Parallelism per KPU
- specify the number of parallel tasks that can be scheduled per KPU for your analytics application.
- Minimum: 1, Maximum: 8

### KPU (Kinesis Processing Units)
- KPUs = (Parallelism) / (Parallelism per KPU)

## Application Monitoring Levels

### Application Monitoring Metrics Level
- Application: Metrics are scoped to the entire application
- Task: Metrics are scoped to each task
- Operator: Metrics are scoped to each operator
- Parallelism: Metrics are scoped to application parallelism

### Application Monitoring Log Level
- Error: Potential catastrophic events of the application
- Warn: Potentially harmful situations of the application
- Info: Informational and transient failure events of the application. recommend logging level
- Debug: Fine-grained informational events that are most useful to debug an application