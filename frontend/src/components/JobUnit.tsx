import { Job } from "../utils/interfaces"
import { TagWrapper } from "./TagWrapper"
import styled from 'styled-components'

const Anchor = styled.a`
  font-size: 16px;

  &, &:visited, &:active {
    text-decoration: none;
    color: #323437;
  }

  &:hover {
    color: grey;
  }
`

interface Props {
  job: Job
}

export const JobUnit = (props: Props) => {
  return (
    <div style={{
      display: "flex", 
      flexDirection: "column", 
      color: "#323437", 
      border: "1px solid #323437",
      borderRadius: "10px",
      padding: "8px",
      boxSizing: "border-box",
      margin: "10px"
    }}>
      <Anchor href={props.job.url}>{"ti"}&nbsp;{">"}&nbsp;{props.job.title}</Anchor>
      <p style={{marginBottom: 0}}>{"co"}&nbsp;{">"}&nbsp;{props.job.company}</p>
      <div style={{"display": "flex", "flexDirection": "row"}}>
        <p>{"sk"}&nbsp;{">"}&nbsp;</p>
        <ul className="skill-tags" style={{padding: 0}}>
          {props.job.skills.map((each, index) => index == 0 ? <TagWrapper style={{"marginLeft": 0}} tag={each} /> : <TagWrapper tag={each} />)}
        </ul>
      </div>
    </div>
  )
}
