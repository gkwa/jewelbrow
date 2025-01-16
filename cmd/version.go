package cmd

import (
	"fmt"
	
	"github.com/spf13/cobra"

	"github.com/gkwa/jewelbrow/version"
)

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version number of jewelbrow",
	Long:  `All software has versions. This is jewelbrow's`,
	Run: func(cmd *cobra.Command, args []string) {
		buildInfo := version.GetBuildInfo()
		fmt.Println(buildInfo)
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)
}
