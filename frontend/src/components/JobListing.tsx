import { Job } from "../utils/interfaces"
import { JobUnit } from "./JobUnit"

interface Props {
  jobs: Array<Job>
}

export const JobListing = (props: Props) => {
  return (
    <div style={{
      display: "flex", 
      flexDirection: "row",
      flexWrap: "wrap",
      justifyContent: "center"
    }}>
      {props.jobs.map(each => {
        return <JobUnit key={each.id} job={each}/>
      })}
    </div>
  )
}
