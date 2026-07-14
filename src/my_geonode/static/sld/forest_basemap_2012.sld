<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
  xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
  xmlns="http://www.opengis.net/sld"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Forest Base Map 2012</Name>
    <UserStyle>
      <Title>Forest Base Map 2012</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ChannelSelection>
              <GrayChannel>
                <SourceChannelName>1</SourceChannelName>
              </GrayChannel>
            </ChannelSelection>
            <ColorMap type="values">
              <ColorMapEntry color="#006400" quantity="1" label="Primary Forest" opacity="1"/>
              <ColorMapEntry color="#228B22" quantity="2" label="Secondary Forest" opacity="1"/>
              <ColorMapEntry color="#90EE90" quantity="3" label="Forest Plantation" opacity="1"/>
              <ColorMapEntry color="#8B4513" quantity="4" label="Non-Forest" opacity="1"/>
              <ColorMapEntry color="#FFD700" quantity="5" label="Agriculture" opacity="1"/>
              <ColorMapEntry color="#4169E1" quantity="6" label="Water" opacity="1"/>
              <ColorMapEntry color="#808080" quantity="7" label="Other Land" opacity="1"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>