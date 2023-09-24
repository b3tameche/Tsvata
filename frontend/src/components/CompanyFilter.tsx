import { useAutocomplete } from '@mui/base/useAutocomplete';
import CheckIcon from '@mui/icons-material/Check';
import { styled } from '@mui/material/styles';
import { autocompleteClasses } from '@mui/material/Autocomplete';

const Root = styled('div')(`
    color: #323437;
    font-size: 14px;
  `,
);

const InputWrapper = styled('div')(`
    width: 300px;
    border: 1px solid #323437;
    background-color: #ffffff;
    border-radius: 4px;
    padding: 1px;
    display: flex;
    flex-wrap: wrap;

    &:hover {
      border-color: #acb6c2;
    }

    &.focused {
      border-color: #323437;
    }

    & input {
      background-color: white;
      color: #323437;
      height: 30px;
      box-sizing: border-box;
      padding: 4px 6px;
      width: 0;
      min-width: 30px;
      flex-grow: 1;
      border: 0;
      margin: 0;
      outline: 0;
    }
  `,
);

const Listbox = styled('ul')(`
    width: 300px;
    margin: 2px 0 0;
    padding: 0;
    position: absolute;
    list-style: none;
    background-color: white;
    overflow: auto;
    max-height: 250px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 1;

    & li {
      padding: 5px 12px;
      display: flex;

      & span {
        flex-grow: 1;
      }

      & svg {
        color: white;
      }
    }

    & li[aria-selected='true'] {
      background-color: #fcdefc;

      & svg {
        color: currentColor;
      }
    }

    & li.${autocompleteClasses.focused} {
      background-color: #fcdefc;
      cursor: pointer;

      & svg {
        color: currentColor;
      }
    }
  `,
);

interface Props {
  companies: Array<string>
  onChange: Function
}

export const CompanyFilter = (props: Props) => {
  const {
    getRootProps,
    getInputProps,
    getListboxProps,
    getOptionProps,
    groupedOptions,
    focused,
    setAnchorEl,
  } = useAutocomplete({
    id: 'company-filter',
    options: props.companies,
    getOptionLabel: (option) => option,
    onChange: (_, value) => value == null ? props.onChange("") : props.onChange(value)
  });

  return (
    <Root>
      <div {...getRootProps()}>
        <InputWrapper ref={setAnchorEl} className={focused ? 'focused' : ''}>
          <input {...getInputProps()} placeholder='Company' style={{fontFamily: "Iosevka Curly"}} />
        </InputWrapper>
      </div>
      {groupedOptions.length > 0 ? (
        <Listbox {...getListboxProps()}>
          {(groupedOptions as typeof props.companies).map((option, index) => (
            <li {...getOptionProps({option, index})}>
              <span>{option}</span>
              <CheckIcon fontSize="small" />
            </li>
          ))}
        </Listbox>
      ) : null}
    </Root>
  );
}