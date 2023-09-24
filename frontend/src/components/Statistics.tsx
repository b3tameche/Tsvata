import styled from "styled-components"
import { Company, Job } from "../utils/interfaces"

const Anchor = styled.a`
  font-size: 16px;
  text-decoration: none;
  color: #323437;
  margin: 0;
  width: 200px;
  box-sizing: border-box;

  &:hover {
    color: grey;
  }
`

interface Props {
  jobs: Array<Job>
  companies: Array<Company>
}

export const Statistics = (props: Props) => {

  const dict: {[company: string]: number} = {}

  props.jobs.forEach(each => {
    if (each.company in dict) {
      dict[each.company]++
    } else {
      dict[each.company] = 1
    }
  })

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      color: "#323437"
    }}>
      <div style={{
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
        justifyContent: "flex-start",
        width: "800px"
      }}>
        {props.companies.map(each => <Anchor href={each.company_website}>{each.company_name} - {dict[each.company_name] || 0}</Anchor>)}
      </div>
    </div>
  )
}
