package senketsu

import (
	"./paths"
	"github.com/fabioberger/airtable-go"
)

type airtableMediaLocation struct {
	AirtableID string              `json:"id,omitempty"`
	Fields     paths.MediaLocation `json:"fields"`
}

func OpenConnection(apiKey, baseID string) (*airtable.Client, error) {
	client, err := airtable.New(apiKey, baseID)
	if err != nil {
		return nil, err
	}
	return client, nil
}

func GetMediaLocations(tableName string, client *airtable.Client) []paths.MediaLocation {
	var records []airtableMediaLocation
	if err := client.ListRecords(tableName, &records); err != nil {
		return []paths.MediaLocation{}
	}
	var locs []paths.MediaLocation
	for i := range records {
		if len(records[i].Fields.Name) > 0 {
			locs = append(locs, records[i].Fields)
		}
	}
	return locs
}

func CreateMediaLocation(location paths.MediaLocation, tableName string, client *airtable.Client) (string, error) {
	record := airtableMediaLocation{Fields: location}
	err := client.CreateRecord(tableName, &record)
	return record.AirtableID, err
}
