import { DropdownButton, Dropdown } from "react-bootstrap";

const SplitButtonDropdown = () => {
  return (
    <DropdownButton id="split-button-dropdown" title="Dropdown Title">
      <Dropdown.Item eventKey="1">Dropdown Item 1</Dropdown.Item>
      <Dropdown.Item eventKey="2">Dropdown Item 2</Dropdown.Item>
      <Dropdown.Item eventKey="3">Dropdown Item 3</Dropdown.Item>
      <Dropdown.Divider />
      <Dropdown.Item eventKey="4">Dropdown Item 4</Dropdown.Item>
    </DropdownButton>
  );
};

export default Dropdown;